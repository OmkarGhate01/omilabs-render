"""Upload the QA-passed package to the Omilabs channel via YouTube Data API v3 (device-flow OAuth).

  python3 youtube_upload.py auth            -> prints a google.com/device code, waits for Allow, saves token
  python3 youtube_upload.py whoami          -> shows which channel the token belongs to (sanity check)
  python3 youtube_upload.py upload 1 2 ...  -> scheduled upload: video + thumbnail + captions + playlist
  python3 youtube_upload.py status          -> what has been uploaded so far

Secrets live only in /root/.secrets (chmod 600) and are never printed or committed.
State (video ids per episode) is in Published-Assets/youtube-upload/uploaded.json, so reruns resume
and never upload the same episode twice.
"""
import sys, os, json, time, csv, datetime, requests

R = os.environ.get("OMI_ROOT", "/home/claude/Bolna-AI-Masterclass/")
PKG = R + "Published-Assets/youtube-upload/"
SEC = os.environ.get("OMI_SECRETS", "/root/.secrets/")
CLIENT, TOKEN = SEC + "yt_client.json", SEC + "yt_token.json"
STATE = PKG + "uploaded.json"
SCOPE = "https://www.googleapis.com/auth/youtube"
API = "https://www.googleapis.com/youtube/v3/"
UPL = "https://www.googleapis.com/upload/youtube/v3/"
PLAYLIST_TITLE = "Bolna AI Masterclass (Full Course)"
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


def long_time(n):
    """Episode publish slot (IST): ep01 15 Oct 19:00, then two a day from 16 Oct, even eps 12:00, odd eps 19:00."""
    if n == 1:
        return datetime.datetime(2026, 10, 15, 19, 0, tzinfo=IST)
    d = datetime.datetime(2026, 10, 16, tzinfo=IST) + datetime.timedelta(days=(n - 2) // 2)
    return d.replace(hour=12) if n % 2 == 0 else d.replace(hour=19)


def reschedule(n):
    """Move an already-uploaded episode to its current slot (costs no upload)."""
    st = jload(STATE, {}); key = "ep%02d" % n; vid = st[key]["video"]
    when = long_time(n).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cur = call("GET", API + "videos", params={"part": "status", "id": vid})["items"][0]["status"]
    if cur.get("publishAt") == when.replace("Z", ".000Z") or cur.get("publishAt") == when:
        return
    body = {"id": vid, "status": {"privacyStatus": "private", "publishAt": when, "selfDeclaredMadeForKids": False,
                                  "embeddable": True, "license": "youtube", "publicStatsViewable": cur.get("publicStatsViewable", True)}}
    v = call("PUT", API + "videos", params={"part": "status"}, json=body)
    st[key]["verified"] = v["status"]; jsave(STATE, st)
    log("%s RESCHEDULED privacy=%s publishAt=%s" % (key, v["status"]["privacyStatus"], v["status"].get("publishAt")))


def jload(p, d=None):
    return json.load(open(p)) if os.path.exists(p) else d


def jsave(p, d, secret=False):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        json.dump(d, f, indent=1)
    if secret:
        os.chmod(p, 0o600)


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    open(PKG + "upload.log", "a").write(line + "\n")


def have(path):
    """File exists locally, or (GitHub runner) is listed as a release asset."""
    if os.path.exists(path):
        return True
    lst = os.environ.get("OMI_ASSET_LIST")
    return bool(lst) and os.path.basename(path) in open(lst).read().split()


def need(path):
    """On the GitHub runner, rebuild the video from branch media/<file> (<=45 MB parts) right before uploading it."""
    if not os.path.exists(path) and os.environ.get("OMI_CI"):
        import subprocess
        name = os.path.basename(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        g = lambda *a: subprocess.run(["git"] + list(a), cwd=R, check=True, capture_output=True).stdout
        g("fetch", "-q", "--depth", "1", "origin", "refs/heads/media/" + name)
        with open(path + ".tmp", "wb") as out:
            for part in sorted(g("ls-tree", "--name-only", "FETCH_HEAD").decode().split()):
                out.write(g("show", "FETCH_HEAD:" + part))
        os.replace(path + ".tmp", path)
    return path


# ---------------- auth ----------------
def auth():
    c = jload(CLIENT)
    r = requests.post("https://oauth2.googleapis.com/device/code", data={"client_id": c["client_id"], "scope": SCOPE}).json()
    if "user_code" not in r:
        sys.exit("device/code failed: %s" % r.get("error", r))
    print("OPEN: %s\nCODE: %s" % (r["verification_url"], r["user_code"]), flush=True)
    end = time.time() + r["expires_in"]
    while time.time() < end:
        time.sleep(r.get("interval", 5))
        t = requests.post("https://oauth2.googleapis.com/token", data={
            "client_id": c["client_id"], "client_secret": c["client_secret"], "device_code": r["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}).json()
        if "access_token" in t:
            t["obtained"] = time.time()
            jsave(TOKEN, t, secret=True)
            print("AUTH OK (token saved, not printed)")
            return
        if t.get("error") not in ("authorization_pending", "slow_down"):
            sys.exit("auth failed: %s" % t.get("error"))
    sys.exit("code expired, run auth again")


def bearer():
    t, c = jload(TOKEN), jload(CLIENT)
    if not t:
        sys.exit("no token: run auth")
    if time.time() > t["obtained"] + t["expires_in"] - 120:
        r = requests.post("https://oauth2.googleapis.com/token", data={
            "client_id": c["client_id"], "client_secret": c["client_secret"],
            "refresh_token": t["refresh_token"], "grant_type": "refresh_token"}).json()
        if "access_token" not in r:
            sys.exit("refresh failed (%s): run auth again" % r.get("error"))
        t.update(access_token=r["access_token"], expires_in=r["expires_in"], obtained=time.time())
        jsave(TOKEN, t, secret=True)
    return {"Authorization": "Bearer " + t["access_token"]}


def call(method, url, **kw):
    for attempt in range(5):
        r = requests.request(method, url, headers={**bearer(), **kw.pop("headers", {})}, timeout=600, **kw)
        if r.status_code in (500, 502, 503, 504):
            time.sleep(2 ** attempt * 3)
            continue
        if r.status_code >= 400:
            try:
                err = r.json()["error"]
                reason = err.get("errors", [{}])[0].get("reason", "")
                raise RuntimeError("%s %s: %s" % (r.status_code, reason, err.get("message", "")[:300]))
            except (ValueError, KeyError):
                raise RuntimeError("%s %s" % (r.status_code, r.text[:300]))
        return r.json() if r.text else {}
    raise RuntimeError("server error after retries")


# ---------------- helpers ----------------
def whoami():
    ch = call("GET", API + "channels", params={"part": "snippet", "mine": "true"})["items"][0]
    print("Channel: %s (%s) id=%s" % (ch["snippet"]["title"], ch["snippet"].get("customUrl", ""), ch["id"]))
    return ch


def playlist_id():
    st = jload(STATE, {})
    if st.get("_playlist"):
        return st["_playlist"]
    page = None
    while True:
        res = call("GET", API + "playlists", params={"part": "snippet", "mine": "true", "maxResults": 50, **({"pageToken": page} if page else {})})
        for p in res.get("items", []):
            if p["snippet"]["title"] == PLAYLIST_TITLE:
                st["_playlist"] = p["id"]; jsave(STATE, st); return p["id"]
        page = res.get("nextPageToken")
        if not page:
            break
    txt = open(PKG + "00-playlist.txt").read()
    desc = txt.split("PLAYLIST DESCRIPTION\n")[1].split("\n\n")[0].strip()
    p = call("POST", API + "playlists", params={"part": "snippet,status"},
             json={"snippet": {"title": PLAYLIST_TITLE, "description": desc, "defaultLanguage": "en"}, "status": {"privacyStatus": "public"}})
    log("playlist created: %s" % p["id"])
    st["_playlist"] = p["id"]; jsave(STATE, st)
    return p["id"]


SEO_TAGS = ["bolna ai tutorial", "bolna ai setup", "ai voice agent", "ai calling agent", "voice ai agent tutorial", "bolna ai voice agent"]


def seo_tags(tags):
    out, n = [], 0
    for t in tags + SEO_TAGS:
        if t.lower() not in [x.lower() for x in out] and n + len(t) + 3 <= 480:
            out.append(t); n += len(t) + 3
    return out


def parse_pkg(n):
    t = open(PKG + "ep%02d-youtube.txt" % n).read()
    title = t.split("TITLE\n")[1].split("\n\n")[0].strip()
    desc = t.split("DESCRIPTION\n")[1].split("\n\nTAGS\n")[0].strip()
    tags = seo_tags([x.strip() for x in t.split("TAGS\n")[1].split("\n")[0].split(",")])
    row = [r for r in csv.DictReader(open(PKG + "schedule.csv")) if int(r["episode"]) == n][0]
    when = datetime.datetime.strptime(row["publish_at"].replace(" IST", ""), "%Y-%m-%d %H:%M").replace(tzinfo=IST)
    try:
        import seo_fixes
        title, desc = seo_fixes.apply(n, title, desc, jload(STATE, {}).get("_playlist"))
    except ImportError:
        pass
    assert len(title) <= 100 and len(desc) <= 5000
    return title, desc, tags, when


def upload(n, when_override=None):
    st = jload(STATE, {})
    key = "ep%02d" % n
    rec = st.get(key, {})
    title, desc, tags, when = parse_pkg(n)
    when = when_override or when
    if when < datetime.datetime.now(IST) + datetime.timedelta(minutes=30):
        raise RuntimeError("publish time %s is too close or past; reschedule first" % when)
    video = R + "Published-Assets/ep%02d-master.mp4" % n
    if not rec.get("video"):
        body = {"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": "27",
                            "defaultLanguage": "en", "defaultAudioLanguage": "en"},
                "status": {"privacyStatus": "private", "publishAt": when.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                           "selfDeclaredMadeForKids": False, "embeddable": True, "license": "youtube"}}
        size = os.path.getsize(need(video))
        init = requests.post(UPL + "videos", params={"uploadType": "resumable", "part": "snippet,status"},
                             headers={**bearer(), "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, json=body, timeout=60)
        if init.status_code >= 400:
            raise RuntimeError("init %s: %s" % (init.status_code, init.text[:300]))
        loc = init.headers["Location"]
        with open(video, "rb") as f:
            r = requests.put(loc, data=f, headers={**bearer(), "Content-Type": "video/mp4", "Content-Length": str(size)}, timeout=3600)
        if r.status_code >= 400:
            raise RuntimeError("upload %s: %s" % (r.status_code, r.text[:300]))
        rec["video"] = r.json()["id"]; st[key] = rec; jsave(STATE, st)
        log("%s uploaded -> %s (scheduled %s)" % (key, rec["video"], when.strftime("%d %b %H:%M IST")))
    vid = rec["video"]
    if not rec.get("thumb"):
        with open(R + "Thumbnails/ep%02d-thumbnail.png" % n, "rb") as f:
            call("POST", UPL + "thumbnails/set", params={"videoId": vid}, headers={"Content-Type": "image/png"}, data=f.read())
        rec["thumb"] = True; st[key] = rec; jsave(STATE, st); log("%s thumbnail set" % key)
    if not rec.get("playlist"):
        call("POST", API + "playlistItems", params={"part": "snippet"},
             json={"snippet": {"playlistId": playlist_id(), "position": n - 1, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
        rec["playlist"] = True; st[key] = rec; jsave(STATE, st); log("%s added to playlist" % key)
    if not rec.get("captions"):
        meta = {"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}}
        bnd = "omilabs-%d" % time.time()
        srt = open(PKG + "ep%02d-en.srt" % n, "rb").read()
        payload = (("--%s\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n%s\r\n--%s\r\nContent-Type: application/octet-stream\r\n\r\n" % (bnd, json.dumps(meta), bnd)).encode()
                   + srt + ("\r\n--%s--" % bnd).encode())
        try:
            call("POST", UPL + "captions", params={"part": "snippet", "uploadType": "multipart"},
                 headers={"Content-Type": "multipart/related; boundary=%s" % bnd}, data=payload)
            rec["captions"] = True; log("%s captions uploaded" % key)
        except RuntimeError as e:
            if "insufficientPermissions" not in str(e):
                raise
            # caption upload needs the youtube.force-ssl scope; captions are already burned into the video
            rec["captions"] = "skipped (scope)"; log("%s captions skipped: token lacks caption scope (burned-in captions present)" % key)
        st[key] = rec; jsave(STATE, st)
    # verify what YouTube actually stored
    v = call("GET", API + "videos", params={"part": "status,snippet", "id": vid})["items"][0]
    log("%s VERIFIED title=%r privacy=%s publishAt=%s upload=%s" % (
        key, v["snippet"]["title"][:50], v["status"]["privacyStatus"], v["status"].get("publishAt"), v["status"].get("uploadStatus")))
    rec["verified"] = v["status"]; st[key] = rec; jsave(STATE, st)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "auth":
        auth()
    elif cmd == "whoami":
        whoami()
    elif cmd == "status":
        for k, v in sorted(jload(STATE, {}).items()):
            print(k, v if k.startswith("_") else {x: v.get(x) for x in ("video", "thumb", "playlist", "captions")})
    elif cmd == "reschedule":
        for n in [int(a) for a in sys.argv[2:]]:
            reschedule(n)
    elif cmd == "upload":
        for n in [int(a) for a in sys.argv[2:]]:
            try:
                upload(n)
            except RuntimeError as e:
                log("ep%02d STOPPED: %s" % (n, e))
                if "uploadLimitExceeded" in str(e) or "quotaExceeded" in str(e):
                    log("daily limit reached; resume tomorrow with the same command")
                    break
