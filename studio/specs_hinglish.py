# 40 Hinglish Shorts (Devanagari Hinglish), facts verified 2026-11-09.
# Sources: about.fb.com Muse launch (Sep 8 2026) + Meta help-centre pricing via tech-insider/layer3labs;
# kling.ai blog "Kling 4.0 vs 3.0" + Kuaishou Oct 15 2026 launch; support.claude.com "Get started with Claude Motion";
# elevenlabs.io/blog/eleven-v4 + ElevenLabs docs (eleven-v4, IVC, dubbing, voice changer, API quickstart).
import json, os, sys

CTA = "Save this — और ऐसे ही AI updates के लिए Omilabs follow करो।"
def cta(): return dict(tag="SAVE THIS", v="cta", d=dict(title="Save this", follow="Omilabs"), say=CTA, hl=["Save", "this", "Omilabs"], chip="Save")
def B(tag, v, d, say, hl=(), chip=""): return dict(tag=tag, v=v, d=d, say=say, hl=list(hl), chip=chip)

S = {}
# ───────────────────────── META MUSE ─────────────────────────
M = "MUSE AI"
S["mu001"] = (M, "Meta Muse AI Kya Hai? Personal AI Agent Explained", [
  B("WHAT", "hook", dict(brand="Meta Muse", pill="PERSONAL AI AGENT", stat="8 Sep", sub="launch 2026"), "Muse AI, Meta का नया personal AI agent है।", ["Muse", "AI", "agent"], "agent"),
  B("NOT A CHATBOT", "versus", dict(bad="Chatbot — सिर्फ जवाब देता है", good="Muse — काम खुद करता है"), "ये सिर्फ जवाब नहीं देता, काम खुद करता है।", ["काम", "खुद"], "खुद"),
  B("TASKS", "list", dict(items=["Emails draft और send", "Travel booking", "Forms भरना", "Goals → action plan"]), "Emails, travel booking, forms भरना, और आपके goals का plan बनाना।", ["Emails", "travel", "forms", "goals"], "goals"),
  B("WHERE", "card", dict(icon="mobile", title="कहाँ चलता है", rows=[["App", "iOS, Android"], ["Web", "muse.ai"], ["Chat", "WhatsApp"]]), "Muse app में या सीधे WhatsApp पर chat करके काम दो।", ["WhatsApp", "app"], "WhatsApp"),
  B("WHO", "stat", dict(value="US", label="अभी सिर्फ United States, 18+"), "अभी ये सिर्फ US में, अठारह साल से ऊपर वालों के लिए है।", ["US", "अठारह"], "US"),
  cta()])
S["mu002"] = (M, "Meta Muse Free Hai? 100 Million Tokens Per Week Explained", [
  B("FREE?", "hook", dict(brand="Meta Muse", pill="FREE TIER", stat="100M", sub="tokens per week"), "Muse AI free है? हाँ, free tier मिलता है।", ["Muse", "free"], "free"),
  B("ALLOWANCE", "stat", dict(value="100M", label="tokens / week (Zuckerberg)"), "Zuckerberg के मुताबिक free में हर हफ्ते सौ million tokens तक।", ["सौ", "million", "tokens"], "million"),
  B("CATCH", "card", dict(icon="lock", title="ध्यान दो", rows=[["Card", "signup पे ज़रूरी"], ["Country", "US only"], ["Age", "18+"]]), "पर signup पे payment card ज़रूरी है, और अभी सिर्फ US में।", ["card", "US"], "card"),
  B("TOKENS", "versus", dict(bad="Chat tokens = agent tokens", good="Agent काम में tokens जल्दी खर्च होते हैं"), "याद रखो, agent के लंबे tasks में tokens जल्दी खर्च होते हैं।", ["agent", "tokens"], "tokens"),
  B("RESET", "card", dict(icon="clock", title="Weekly reset", rows=[["Quota", "हर हफ्ते reset"], ["ज़्यादा चाहिए?", "paid plan"]]), "Quota हर हफ्ते reset होता है, ज़्यादा चाहिए तो paid plan।", ["हफ्ते", "reset"], "reset"),
  cta()])
S["mu003"] = (M, "Meta Muse Plans: Free vs Power $20 vs Maximum $100", [
  B("PLANS", "hook", dict(brand="Meta Muse", pill="PRICING", stat="3", sub="plans"), "Muse AI के तीन plans हैं, कौनसा लें?", ["Muse", "तीन", "plans"], "plans"),
  B("FREE", "card", dict(icon="wallet", title="Free", rows=[["Price", "$0"], ["Tokens", "~100M / week"]]), "Free plan, zero dollar, लगभग सौ million tokens हर हफ्ते।", ["Free", "zero"], "Free"),
  B("POWER", "card", dict(icon="bolt", title="Power", rows=[["Price", "$20 / month"], ["Tokens", "500M / week"]], hl=1), "Power plan, बीस dollar महीना, पाँच सौ million tokens हर हफ्ते।", ["Power", "बीस", "dollar"], "Power"),
  B("MAXIMUM", "card", dict(icon="star", title="Maximum", rows=[["Price", "$100 / month"], ["Tokens", "3B / week"]], hl=1), "Maximum plan, सौ dollar महीना, तीन billion tokens हर हफ्ते।", ["Maximum", "billion"], "Maximum"),
  B("SAME FEATURES", "versus", dict(bad="Paid = extra features", good="Paid = सिर्फ ज़्यादा usage"), "Paid plans में features वही हैं, बस usage ज़्यादा मिलता है।", ["features", "usage"], "usage"),
  cta()])
S["mu004"] = (M, "Meta Muse Kya Kya Kar Sakta Hai? 5 Real Tasks", [
  B("TASKS", "hook", dict(brand="Meta Muse", pill="WHAT IT DOES", stat="5", sub="real tasks"), "Muse AI असल में क्या कर सकता है? पाँच काम देखो।", ["Muse", "पाँच"], "पाँच"),
  B("EMAIL", "card", dict(icon="mail", title="Email", rows=[["Draft", "करता है"], ["Send", "आपकी approval से"]]), "एक, emails draft और send करना।", ["emails"], "emails"),
  B("TRAVEL", "card", dict(icon="globe", title="Travel", rows=[["Flights", "book"], ["Plans", "organize"]]), "दो, travel book करना। तीन, websites पे forms भरना।", ["travel", "forms"], "travel"),
  B("SHOPPING", "card", dict(icon="wallet", title="Shopping", rows=[["Checkout", "Stripe Link से"], ["Approval", "purchase से पहले"]]), "चार, shopping, आपकी approval के साथ।", ["shopping", "approval"], "approval"),
  B("GOALS", "flow", dict(nodes=["Goal बताओ", "Plan बनता है", "Muse काम करता है"]), "पाँच, आपका goal लेकर plan बनाना, और app बंद होने के बाद भी काम चलता रहता है।", ["goal", "plan", "बंद"], "plan"),
  cta()])
S["mu005"] = (M, "Meta Muse Secure VM: Har User Ka Apna Cloud Computer", [
  B("SECURE VM", "hook", dict(brand="Muse Secure VM", pill="SECURITY", stat="1", sub="VM per user"), "Muse AI हर user को अपना cloud computer देता है।", ["Muse", "cloud", "computer"], "computer"),
  B("WHAT", "card", dict(icon="cpu", title="Muse Secure VM", rows=[["Type", "dedicated virtual machine"], ["अंदर", "agent + आपका data"]]), "इसे Muse Secure VM कहते हैं, agent और आपका data इसी में रहता है।", ["Secure", "VM", "data"], "VM"),
  B("ISOLATED", "versus", dict(bad="Shared machine", good="किसी और का agent पहुँच नहीं सकता"), "ये contained है, किसी और का agent इस तक नहीं पहुँच सकता।", ["contained", "नहीं"], "contained"),
  B("PASSWORDS", "card", dict(icon="lock", title="Credentials", rows=[["Storage", "secure store"], ["Agent", "passwords देख नहीं सकता"]]), "Logins secure storage में रहते हैं, agent उन्हें देख नहीं सकता।", ["secure", "देख"], "secure"),
  B("NEXT", "stat", dict(value="Soon", label="Muse Confidential VM — सिर्फ आपकी key"), "आगे Confidential VM आएगा, जिसकी key सिर्फ आपके पास होगी।", ["Confidential", "key"], "key"),
  cta()])
S["mu006"] = (M, "Meta Muse Sentinel Kya Hai? AI Agent Ka Security Guard", [
  B("SENTINEL", "hook", dict(brand="Sentinel", pill="SAFETY", stat="100%", sub="internet actions checked"), "Muse AI का security guard है Sentinel।", ["Muse", "Sentinel"], "Sentinel"),
  B("WHAT", "card", dict(icon="lock", title="Sentinel agent", rows=[["कहाँ", "same VM पे"], ["Separate", "system level पे"]]), "Sentinel एक अलग agent है, उसी machine पे, पर Muse से अलग।", ["अलग", "agent"], "अलग"),
  B("RULE", "versus", dict(bad="Agent सीधे internet पे", good="Sentinel approve करे तभी"), "Muse का कोई भी काम internet तक तभी पहुँचता है जब Sentinel approve करे।", ["Sentinel", "approve"], "approve"),
  B("PERMISSION", "flow", dict(nodes=["Muse action", "Sentinel check", "आपसे permission"]), "ज़रूरत हो तो Sentinel आपसे permission माँगता है।", ["permission"], "permission"),
  B("WHY", "card", dict(icon="check", title="फायदा", rows=[["Purchases", "बिना approval नहीं"], ["Control", "आपके हाथ में"]]), "मतलब control हमेशा आपके हाथ में रहता है।", ["control"], "control"),
  cta()])
S["mu007"] = (M, "Meta Muse Se Shopping Safe Hai? Payments Explained", [
  B("PAYMENTS", "hook", dict(brand="Muse Checkout", pill="PAYMENTS", stat="1x", sub="one-time card"), "Muse AI से shopping safe है? Payment ऐसे काम करता है।", ["Muse", "shopping", "safe"], "safe"),
  B("STRIPE LINK", "card", dict(icon="wallet", title="Stripe Link", rows=[["Checkout", "Link से"], ["Card", "one-time number"]]), "Checkout Stripe Link से होता है, one-time card number के साथ।", ["Stripe", "Link", "one-time"], "one-time"),
  B("APPROVAL", "versus", dict(bad="Agent खुद pay कर दे", good="Purchase से पहले आपकी approval"), "Purchase से पहले approval आपसे ली जाती है।", ["approval"], "approval"),
  B("COMING", "list", dict(items=["Shop Pay — जल्द", "1Password — जल्द"]), "Shop Pay और 1Password support भी जल्द आ रहा है।", ["Shop", "Pay", "1Password"], "जल्द"),
  B("TIP", "card", dict(icon="check", title="Tip", rows=[["हर purchase", "review करो"], ["Log", "audit में देखो"]]), "Tip: हर purchase review करो, और activity log check करो।", ["review", "log"], "review"),
  cta()])
S["mu008"] = (M, "Meta Muse WhatsApp Mein Kaise Use Karein", [
  B("WHATSAPP", "hook", dict(brand="Muse × WhatsApp", pill="CHAT", stat="1", sub="message se काम"), "Muse AI को WhatsApp में use कर सकते हो।", ["Muse", "WhatsApp"], "WhatsApp"),
  B("HOW", "card", dict(icon="chat", title="Chat जैसे", rows=[["Talk", "message भेजो"], ["Muse", "काम करता है"]]), "Muse से बात करना किसी इंसान को message भेजने जैसा है।", ["message"], "message"),
  B("WHERE", "list", dict(items=["Muse app", "WhatsApp", "muse.ai web"]), "Muse app में, WhatsApp में, या muse.ai पे।", ["app", "WhatsApp", "web"], "WhatsApp"),
  B("BACKGROUND", "versus", dict(bad="App बंद = काम बंद", good="App बंद करके भी काम चलता है"), "App बंद करने के बाद भी Muse काम करता रहता है।", ["बंद", "काम"], "बंद"),
  B("REGION", "stat", dict(value="US", label="अभी availability"), "बस ध्यान रहे, अभी ये सिर्फ US में available है।", ["US"], "US"),
  cta()])
S["mu009"] = (M, "Meta Muse India Mein Kab Aayega? Availability 2026", [
  B("INDIA?", "hook", dict(brand="Meta Muse", pill="AVAILABILITY", stat="US", sub="only, for now"), "Muse AI India में use कर सकते हैं? अभी नहीं।", ["Muse", "India", "नहीं"], "नहीं"),
  B("NOW", "card", dict(icon="globe", title="Launch", rows=[["Country", "United States"], ["Age", "18+"], ["Platforms", "iOS, Android, web"]]), "Launch सिर्फ United States में हुआ है, अठारह plus users के लिए।", ["United", "States"], "States"),
  B("DATE", "stat", dict(value="—", label="India date अभी announce नहीं"), "Meta ने India के लिए अभी कोई date announce नहीं की।", ["date", "नहीं"], "date"),
  B("SOON", "list", dict(items=["AI glasses — जल्द", "Confidential VM — इस साल"]), "AI glasses support और Confidential VM जल्द आने वाले हैं।", ["glasses", "Confidential"], "जल्द"),
  B("TIP", "versus", dict(bad="Fake 'Muse India' apps", good="सिर्फ official muse.ai और stores"), "Fake apps से बचो, सिर्फ official source use करो।", ["Fake", "official"], "official"),
  cta()])
S["mu010"] = (M, "Meta Muse AI Complete Beginners Guide 2026", [
  B("GUIDE", "hook", dict(brand="Meta Muse", pill="GUIDE 2026", stat="30s", sub="full guide"), "Muse AI का पूरा guide, तीस seconds में।", ["Muse", "guide"], "guide"),
  B("WHAT", "card", dict(icon="cpu", title="Muse क्या है", rows=[["By", "Meta"], ["Type", "personal AI agent"], ["Model", "Muse Spark"]]), "Meta का personal AI agent, Muse Spark model पे चलता है।", ["Meta", "agent", "Spark"], "agent"),
  B("SAFETY", "list", dict(items=["अपना Secure VM", "Sentinel approvals", "One-time card checkout"]), "अपना Secure VM, Sentinel approvals, और one-time card checkout।", ["VM", "Sentinel", "card"], "Sentinel"),
  B("PRICE", "card", dict(icon="wallet", title="Plans", rows=[["Free", "~100M tokens/week"], ["Power", "$20/mo"], ["Maximum", "$100/mo"]]), "Free tier, Power बीस dollar, Maximum सौ dollar महीना।", ["Free", "Power", "Maximum"], "Free"),
  B("ACCESS", "browser", dict(url="muse.ai", button="Get Muse"), "अभी US में iOS, Android, muse.ai और WhatsApp पे।", ["US", "WhatsApp"], "US"),
  cta()])

# ───────────────────────── KLING 4.0 ─────────────────────────
K = "KLING 4.0"
S["kl001"] = (K, "Kling 4.0 Kya Hai? 30 Second AI Video Generator", [
  B("WHAT", "hook", dict(brand="Kling 4.0", pill="AI VIDEO", stat="30s", sub="per generation"), "Kling 4.0, Kuaishou का नया AI video model है।", ["Kling", "4.0", "AI"], "4.0"),
  B("LAUNCH", "card", dict(icon="video", title="Kling 4.0", rows=[["By", "Kling AI (Kuaishou)"], ["Launch", "15 Oct 2026"], ["Type", "video generation"]]), "पंद्रह October twenty twenty six को launch हुआ।", ["October", "launch"], "launch"),
  B("LENGTH", "stat", dict(value="3–30s", label="एक generation में"), "एक ही generation में तीन से तीस second तक की video।", ["तीस", "second"], "तीस"),
  B("CONTROL", "list", dict(items=["10 keyframes तक", "15 references तक", "Stereo audio"]), "दस keyframes, पंद्रह references, और stereo audio।", ["keyframes", "references", "stereo"], "keyframes"),
  B("INPUT", "versus", dict(bad="सिर्फ text prompt", good="Text + images + videos + keyframes"), "Text के साथ images, videos और keyframes से direct करो।", ["images", "videos", "keyframes"], "direct"),
  cta()])
S["kl002"] = (K, "Kling 4.0 Account Kaise Banayein Aur Pehla Video", [
  B("START", "hook", dict(brand="Kling 4.0", pill="GET STARTED", stat="3", sub="steps"), "Kling 4.0 पे पहला video, तीन steps में।", ["Kling", "पहला", "video"], "video"),
  B("STEP 1", "browser", dict(url="kling.ai", button="Sign In"), "पहले kling dot ai खोलो और sign in करो।", ["kling", "dot", "ai"], "kling"),
  B("STEP 2", "card", dict(icon="video", title="Model चुनो", rows=[["Kling 4.0", "3–30 sec"], ["4.0 Flash", "3–20 sec, faster"]], hl=0), "Model में Kling 4.0 या तेज़ वाला 4.0 Flash चुनो।", ["4.0", "Flash"], "Flash"),
  B("STEP 3", "flow", dict(nodes=["Prompt लिखो", "Duration चुनो", "Generate"]), "Prompt लिखो, duration चुनो, generate करो।", ["Prompt", "duration", "generate"], "generate"),
  B("CREDITS", "card", dict(icon="wallet", title="Credits", rows=[["लंबी video", "ज़्यादा credits"], ["Check", "generate से पहले estimate"]]), "लंबी video में ज़्यादा credits लगते हैं, पहले estimate देखो।", ["credits", "estimate"], "estimate"),
  cta()])
S["kl003"] = (K, "Kling 4.0 Image To Video: Photo Ko Animate Karo", [
  B("IMG→VIDEO", "hook", dict(brand="Kling 4.0", pill="IMAGE TO VIDEO", stat="10", sub="keyframes तक"), "Kling 4.0 से photo को video में बदलो।", ["Kling", "photo", "video"], "photo"),
  B("FIRST FRAME", "card", dict(icon="image", title="First frame", rows=[["Upload", "अपनी photo"], ["Kling", "उसी से start"]]), "Photo को first frame बनाओ, video वहीं से शुरू होगी।", ["first", "frame"], "frame"),
  B("LAST FRAME", "card", dict(icon="image", title="Last frame", rows=[["Optional", "ending image"], ["Result", "start → end motion"]]), "चाहो तो last frame भी दो, Kling बीच की motion बनाएगा।", ["last", "motion"], "motion"),
  B("PROMPT", "versus", dict(bad="सिर्फ photo, no prompt", good="Photo + motion prompt (क्या हिले)"), "साथ में लिखो क्या हिलना चाहिए, camera कैसे चले।", ["हिलना", "camera"], "camera"),
  B("FLASH", "stat", dict(value="Flash", label="सिर्फ first frame support"), "ध्यान दो, 4.0 Flash में सिर्फ first frame चलता है।", ["Flash", "first"], "Flash"),
  cta()])
S["kl004"] = (K, "Kling 4.0 Mein 30 Second Videos: 3.0 Se Double", [
  B("30 SEC", "hook", dict(brand="Kling 4.0", pill="LONGER CLIPS", stat="30s", sub="native"), "Kling 4.0 में एक बार में तीस second की video।", ["Kling", "तीस", "second"], "तीस"),
  B("BEFORE", "versus", dict(bad="Kling 3.0: 3–15 sec", good="Kling 4.0: 3–30 sec"), "Kling 3.0 पंद्रह second तक था, 4.0 तीस तक जाता है।", ["पंद्रह", "तीस"], "तीस"),
  B("WHY", "card", dict(icon="video", title="फायदा", rows=[["Single take", "बिना stitching"], ["Ads", "पूरा spot एक में"]]), "मतलब बिना जोड़ तोड़ के पूरा scene एक ही take में।", ["take", "scene"], "take"),
  B("FLASH", "card", dict(icon="bolt", title="4.0 Flash", rows=[["Length", "3–20 sec"], ["Speed", "faster"]]), "Flash version बीस second तक, पर तेज़ है।", ["Flash", "बीस"], "Flash"),
  B("TIP", "stat", dict(value="5s", label="पहले छोटा test, फिर 30s"), "Tip: पहले छोटा test बनाओ, फिर full तीस second।", ["test"], "test"),
  cta()])
S["kl005"] = (K, "Kling 4.0 Perfect Prompt Kaise Likhein", [
  B("PROMPT", "hook", dict(brand="Kling 4.0", pill="PROMPTING", stat="4", sub="parts"), "Kling 4.0 के लिए perfect prompt का formula।", ["Kling", "prompt", "formula"], "formula"),
  B("FORMULA", "list", dict(items=["Subject — कौन/क्या", "Action — क्या हो रहा", "Camera — कैसे move", "Light — mood"]), "Subject, action, camera और lighting, ये चार चीज़ें।", ["Subject", "action", "camera", "lighting"], "camera"),
  B("EXAMPLE", "card", dict(icon="edit", title="Example", rows=[["Subject", "chai वाला, Mumbai"], ["Action", "चाय डालता है"], ["Camera", "slow push in"], ["Light", "golden hour"]]), "जैसे, Mumbai का चाय वाला, slow push in, golden hour।", ["slow", "golden"], "golden"),
  B("VAGUE", "versus", dict(bad="'एक अच्छी video बनाओ'", good="हर detail साफ-साफ लिखो"), "Vague prompt मत लिखो, हर detail साफ लिखो।", ["Vague", "detail"], "detail"),
  B("REFS", "stat", dict(value="15", label="references तक जोड़ सकते हो"), "और ज़रूरत हो तो पंद्रह references तक जोड़ो।", ["पंद्रह", "references"], "references"),
  cta()])
S["kl006"] = (K, "Kling 4.0 vs Kling 3.0: Kya Badla?", [
  B("4 vs 3", "hook", dict(brand="Kling 4.0", pill="VS 3.0", stat="4", sub="big upgrades"), "Kling 4.0 और 3.0 में क्या बदला?", ["Kling", "4.0", "3.0"], "4.0"),
  B("LENGTH", "versus", dict(bad="3.0: 15 sec तक", good="4.0: 30 sec तक"), "Length, पंद्रह से तीस second।", ["पंद्रह", "तीस"], "तीस"),
  B("KEYFRAMES", "versus", dict(bad="3.0: start और end frame", good="4.0: 10 keyframes तक"), "Keyframes, start end से बढ़कर दस तक।", ["दस", "keyframes"], "दस"),
  B("REFERENCES", "card", dict(icon="image", title="Omni Reference", rows=[["Total", "15 assets"], ["Images", "10 तक"], ["Videos", "5 (30 sec total)"]]), "Omni Reference में पंद्रह assets, दस images, पाँच videos।", ["Omni", "पंद्रह"], "Omni"),
  B("AUDIO", "list", dict(items=["Two-channel stereo", "Multilingual lip sync", "Video editing"]), "साथ में stereo audio, lip sync और video editing।", ["stereo", "lip", "sync"], "stereo"),
  cta()])
S["kl007"] = (K, "Kling 4.0 Camera Movements: Cinematic Shots Kaise Banayein", [
  B("CAMERA", "hook", dict(brand="Kling 4.0", pill="CINEMATIC", stat="10", sub="keyframes"), "Kling 4.0 में cinematic camera shots ऐसे बनाओ।", ["Kling", "cinematic", "camera"], "camera"),
  B("WORDS", "list", dict(items=["Slow push in", "Pan left / right", "Tracking shot", "Orbit shot"]), "Prompt में लिखो: slow push in, pan, tracking या orbit shot।", ["push", "tracking", "orbit"], "orbit"),
  B("STABLE", "card", dict(icon="video", title="4.0 focus", rows=[["Motion", "ज़्यादा stable"], ["Tracking/orbit", "smoother"]]), "Kling 4.0 का focus है stable motion और smooth tracking, orbit shots।", ["stable", "smooth"], "stable"),
  B("KEYFRAMES", "flow", dict(nodes=["Keyframe 1", "Keyframe 2", "… 10 तक"]), "Shot कहाँ जाए, ये keyframes से pin करो।", ["keyframes", "pin"], "pin"),
  B("COMBINE", "versus", dict(bad="सिर्फ camera word", good="Camera + subject + light एक prompt में"), "Camera, subject और light को एक prompt में जोड़ो।", ["Camera", "subject", "light"], "जोड़ो"),
  cta()])
S["kl008"] = (K, "Kling 4.0 Se Product Videos Kaise Banayein", [
  B("PRODUCT", "hook", dict(brand="Kling 4.0", pill="PRODUCT ADS", stat="15", sub="references"), "Kling 4.0 से product video कैसे बनाएँ?", ["Kling", "product", "video"], "product"),
  B("PHOTOS", "card", dict(icon="image", title="Product photos", rows=[["Angles", "अलग-अलग"], ["Background", "clean"]]), "Product की साफ photos लो, अलग अलग angles से।", ["photos", "angles"], "angles"),
  B("OMNI", "card", dict(icon="star", title="Omni Reference", rows=[["Images", "10 तक"], ["Same product", "हर shot में"]]), "Omni Reference में ये images डालो, product हर shot में same रहेगा।", ["Omni", "same"], "same"),
  B("PROMPT", "list", dict(items=["Product + surface", "Movement (orbit)", "Lighting", "Commercial style"]), "Prompt: product, surface, movement, lighting, commercial style।", ["movement", "lighting"], "lighting"),
  B("LENGTH", "stat", dict(value="30s", label="पूरा ad एक generation में"), "तीस second में पूरा ad एक ही बार में।", ["तीस", "ad"], "ad"),
  cta()])
S["kl009"] = (K, "Kling 4.0 Keyframes: 10 Frames Se Video Direct Karo", [
  B("KEYFRAMES", "hook", dict(brand="Kling 4.0", pill="MULTI-KEYFRAME", stat="10", sub="keyframes"), "Kling 4.0 में दस keyframes से video direct करो।", ["Kling", "दस", "keyframes"], "keyframes"),
  B("WHAT", "card", dict(icon="image", title="Keyframe", rows=[["Image", "किसी moment की"], ["Kling", "बीच की motion भरता है"]]), "Keyframe मतलब किसी moment की image, बीच की motion Kling भरता है।", ["moment", "motion"], "motion"),
  B("STORYBOARD", "flow", dict(nodes=["Start", "Action", "Reveal", "End"]), "जैसे storyboard: start, action, reveal, end।", ["storyboard"], "storyboard"),
  B("USE", "list", dict(items=["Camera moves", "Shot changes", "Character actions"]), "Camera moves, shot changes और character actions control होते हैं।", ["Camera", "shot", "control"], "control"),
  B("FLASH", "versus", dict(bad="4.0 Flash: keyframes नहीं", good="Kling 4.0: 10 keyframes"), "Keyframes के लिए full 4.0 चुनो, Flash में ये नहीं है।", ["full", "Flash"], "full"),
  cta()])
S["kl010"] = (K, "Kling 4.0 Complete Beginners Guide 2026", [
  B("GUIDE", "hook", dict(brand="Kling 4.0", pill="GUIDE 2026", stat="30s", sub="full guide"), "Kling 4.0 का पूरा guide, तीस seconds में।", ["Kling", "guide"], "guide"),
  B("WHAT", "card", dict(icon="video", title="Kling 4.0", rows=[["By", "Kuaishou"], ["Launch", "15 Oct 2026"], ["Length", "3–30 sec"]]), "Kuaishou का AI video model, तीन से तीस second clips।", ["Kuaishou", "तीस"], "तीस"),
  B("FEATURES", "list", dict(items=["Text / image to video", "10 keyframes", "15 references", "Stereo audio"]), "Text और image to video, दस keyframes, पंद्रह references, stereo audio।", ["keyframes", "references"], "keyframes"),
  B("MODELS", "versus", dict(bad="4.0 Flash: fast, 20s, first frame", good="Kling 4.0: full control, 30s"), "Speed चाहिए तो Flash, full control चाहिए तो 4.0।", ["Flash", "control"], "control"),
  B("START", "browser", dict(url="kling.ai", button="Create"), "kling dot ai पे जाओ और पहली video बनाओ।", ["kling", "dot", "ai"], "kling"),
  cta()])

# ───────────────────────── CLAUDE MOTION ─────────────────────────
C = "CLAUDE MOTION"
S["cm001"] = (C, "Claude Motion Kya Hai? Anthropic Ka Animation Tool", [
  B("WHAT", "hook", dict(brand="Claude Motion", pill="ANIMATION", stat="8 Oct", sub="beta launch 2026"), "Claude Motion, Anthropic का नया animation feature है।", ["Claude", "Motion", "animation"], "animation"),
  B("HOW", "card", dict(icon="code", title="Code से animation", rows=[["Claude", "code लिखता है"], ["Animate", "text, charts, shapes, images"]]), "Claude code लिखकर text, charts और images को animate करता है।", ["code", "animate"], "code"),
  B("NOT VIDEO AI", "versus", dict(bad="Video generation model", good="Code-driven animation"), "ये video generation model नहीं है, इसलिए realistic लोग नहीं बनाता।", ["नहीं", "realistic"], "नहीं"),
  B("USE", "list", dict(items=["All-hands explainer", "Board deck chart", "Onboarding walkthrough"]), "Explainers, animated charts और product walkthroughs के लिए बढ़िया।", ["Explainers", "charts"], "charts"),
  B("PLANS", "stat", dict(value="Beta", label="Team और Enterprise plans"), "अभी ये Team और Enterprise plans पे beta में है।", ["Team", "Enterprise"], "beta"),
  cta()])
S["cm002"] = (C, "Claude Motion Se Pehla Animation Kaise Banayein", [
  B("FIRST", "hook", dict(brand="Claude Motion", pill="HOW TO", stat="2", sub="ways to start"), "Claude Motion में पहला animation ऐसे बनाओ।", ["Claude", "Motion", "पहला"], "पहला"),
  B("WAY 1", "flow", dict(nodes=["Chat खोलो", "Output", "Motion"]), "Chat में message box से Output चुनो, फिर Motion।", ["Output", "Motion"], "Output"),
  B("WAY 2", "card", dict(icon="star", title="Artifacts tab", rows=[["Open", "Artifacts"], ["Pick", "Motion template"]]), "या Artifacts tab में Motion template चुनो।", ["Artifacts", "template"], "template"),
  B("DESCRIBE", "list", dict(items=["कौन देखेगा", "कहाँ चलेगा", "कितना लंबा"]), "बताओ कौन देखेगा, कहाँ चलेगा, और कितना लंबा हो।", ["कौन", "कहाँ", "लंबा"], "लंबा"),
  B("ATTACH", "card", dict(icon="image", title="Attach करो", rows=[["Report", "PDF / doc"], ["Data", "numbers"], ["Images", "brand assets"]]), "अपनी report, data या images attach करो।", ["report", "data", "images"], "data"),
  cta()])
S["cm003"] = (C, "Claude Motion Prompts Jo Actually Kaam Karte Hain", [
  B("PROMPTS", "hook", dict(brand="Claude Motion", pill="PROMPTING", stat="3", sub="must-haves"), "Claude Motion के prompts जो सच में काम करते हैं।", ["Claude", "Motion", "prompts"], "prompts"),
  B("RULE", "versus", dict(bad="'pricing को animate करो'", good="'20 sec clip, sales kickoff, 3 plans left to right'"), "Vague नहीं, specific लिखो: audience, length, क्या दिखाना है।", ["specific", "length"], "specific"),
  B("CONTEXT", "list", dict(items=["Audience बताओ", "कहाँ play होगा", "लगभग duration"]), "Anthropic की tip: audience, जगह और duration ज़रूर बताओ।", ["audience", "duration"], "audience"),
  B("DATA", "card", dict(icon="chart", title="अपना content दो", rows=[["Motion", "जो दोगे वही animate"], ["Best", "report + data + images"]]), "Motion वही animate करता है जो आप देते हो, तो data attach करो।", ["data", "attach"], "data"),
  B("ITERATE", "flow", dict(nodes=["Draft", "Feedback", "Final"]), "पहला draft लो, फिर chat में बदलाव बताओ।", ["draft", "बदलाव"], "draft"),
  cta()])
S["cm004"] = (C, "Claude Motion Kaun Use Kar Sakta Hai? Plans Explained", [
  B("ACCESS", "hook", dict(brand="Claude Motion", pill="WHO CAN USE", stat="2", sub="plans"), "Claude Motion कौन use कर सकता है?", ["Claude", "Motion", "कौन"], "कौन"),
  B("PLANS", "card", dict(icon="users", title="Beta access", rows=[["Team", "on by default"], ["Enterprise", "owner on करे"]]), "Team plans पे ये default on है, Enterprise पे owner को on करना होता है।", ["Team", "Enterprise", "owner"], "Team"),
  B("ADMIN", "flow", dict(nodes=["Organization settings", "Artifacts", "Motion on"]), "Setting है: Organization settings में Artifacts।", ["Organization", "Artifacts"], "Artifacts"),
  B("LIMITS", "card", dict(icon="clock", title="Usage", rows=[["Counts", "plan limit में"], ["लंबा animation", "ज़्यादा usage"]]), "ये आपकी plan limit में count होता है, लंबा animation ज़्यादा लेता है।", ["limit", "ज़्यादा"], "limit"),
  B("PRICE", "stat", dict(value="$0", label="अलग price नहीं — plan में शामिल"), "Motion की अलग price नहीं है, ये plan में ही आता है।", ["price", "plan"], "plan"),
  cta()])
S["cm005"] = (C, "Claude Motion vs AI Video Generators: Kya Fark Hai?", [
  B("VS", "hook", dict(brand="Claude Motion", pill="VS VIDEO AI", stat="2", sub="different tools"), "Claude Motion और AI video generators में क्या फर्क है?", ["Claude", "Motion", "फर्क"], "फर्क"),
  B("MOTION", "card", dict(icon="code", title="Claude Motion", rows=[["Method", "code-driven"], ["Best", "charts, explainers"], ["Edit", "एक word / number"]]), "Motion code से बनता है, charts और explainers के लिए।", ["code", "charts"], "code"),
  B("VIDEO AI", "card", dict(icon="video", title="Video generators", rows=[["Method", "video model"], ["Best", "realistic footage"], ["Example", "Kling, Runway"]]), "Video generators realistic footage बनाते हैं, जैसे Kling या Runway।", ["realistic", "footage"], "realistic"),
  B("PICK", "versus", dict(bad="Talking head चाहिए → Motion नहीं", good="Data / explainer → Motion"), "Data और explainer चाहिए तो Motion, असली लोग चाहिए तो video tool।", ["Data", "explainer"], "explainer"),
  B("HANDOFF", "list", dict(items=["Adobe", "Descript", "HeyGen", "Runway", "Luma AI"]), "Motion का animation Adobe, Descript, HeyGen, Runway जैसे tools में आगे ले जा सकते हो।", ["Adobe", "Runway"], "आगे"),
  cta()])
S["cm006"] = (C, "Claude Motion Se Data Ko Animated Chart Banao", [
  B("CHARTS", "hook", dict(brand="Claude Motion", pill="ANIMATED CHART", stat="1", sub="prompt"), "Claude Motion से data को animated chart बनाओ।", ["Claude", "Motion", "chart"], "chart"),
  B("ATTACH", "card", dict(icon="chart", title="Data दो", rows=[["Report", "attach"], ["Numbers", "जो animate हों"]]), "पहले अपनी report या data attach करो।", ["report", "data"], "data"),
  B("ASK", "card", dict(icon="edit", title="Prompt", rows=[["What", "growth chart"], ["For", "board deck"], ["Length", "~20 sec"]]), "फिर लिखो: board deck के लिए growth chart, बीस second।", ["growth", "chart"], "growth"),
  B("EDIT", "versus", dict(bad="पूरा दोबारा बनाओ", good="सिर्फ एक number बदलो"), "Code है, इसलिए एक number बदलो, बाकी सब वैसा ही रहता है।", ["number", "बाकी"], "number"),
  B("EXPORT", "stat", dict(value="MP4", label="export करो, deck में लगाओ"), "MP4 export करो और deck में लगाओ।", ["MP4", "export"], "MP4"),
  cta()])
S["cm007"] = (C, "Claude Motion Animation Edit Kaise Karein", [
  B("EDIT", "hook", dict(brand="Claude Motion", pill="EDITING", stat="2", sub="ways to edit"), "Claude Motion में animation edit करने के दो तरीके।", ["Claude", "Motion", "edit"], "edit"),
  B("CHAT", "card", dict(icon="chat", title="Chat से", rows=[["बोलो", "scene timing बदलो"], ["या", "number बदलो"]]), "एक, chat में बोलो: scene की timing या number बदलो।", ["chat", "timing"], "chat"),
  B("EDITOR", "card", dict(icon="edit", title="Editor में", rows=[["Direct", "खुद change करो"], ["Text", "word बदलो"]]), "दो, editor में direct खुद बदलाव करो।", ["editor", "direct"], "editor"),
  B("WHY", "versus", dict(bad="Video: छोटा change = re-render सब", good="Motion: एक detail बदलो, बाकी same"), "क्योंकि ये code है, एक detail बदलती है, बाकी same रहता है।", ["code", "same"], "code"),
  B("SAVE", "stat", dict(value="Artifact", label="Artifacts tab में saved"), "हर animation Artifacts tab में save रहता है।", ["Artifacts"], "Artifacts"),
  cta()])
S["cm008"] = (C, "Claude Motion Export Aur Share Kaise Karein", [
  B("EXPORT", "hook", dict(brand="Claude Motion", pill="EXPORT", stat="MP4", sub="format"), "Claude Motion से export और share कैसे करें?", ["Claude", "Motion", "export"], "export"),
  B("FORMAT", "stat", dict(value="MP4", label="Export format — सिर्फ MP4"), "Export का format एक ही है, MP4।", ["MP4"], "MP4"),
  B("PRIVATE", "versus", dict(bad="Default में सब देख सकते हैं", good="Default में सिर्फ आप"), "Animation default में private रहता है, सिर्फ आपके लिए।", ["private"], "private"),
  B("SHARE", "flow", dict(nodes=["Animation खोलो", "Share", "Team को भेजो"]), "Share करना है तो animation खोलो और Share click करो।", ["Share"], "Share"),
  B("NEXT TOOLS", "list", dict(items=["Adobe", "Descript", "HeyGen", "invideo", "Canva (soon)"]), "आगे edit के लिए Adobe, Descript, HeyGen में खोल सकते हो।", ["Adobe", "Descript", "HeyGen"], "Adobe"),
  cta()])
S["cm009"] = (C, "Claude Motion Ki 3 Limits Jo Pata Honi Chahiye", [
  B("LIMITS", "hook", dict(brand="Claude Motion", pill="LIMITS", stat="3", sub="things to know"), "Claude Motion की तीन limits जो पता होनी चाहिए।", ["Claude", "Motion", "limits"], "limits"),
  B("LIMIT 1", "card", dict(icon="warning", title="No realistic footage", rows=[["Video model", "नहीं"], ["असली लोग", "नहीं बनते"]]), "एक, ये realistic footage या असली लोग नहीं बनाता।", ["realistic", "असली"], "realistic"),
  B("LIMIT 2", "card", dict(icon="users", title="Plans", rows=[["Team", "beta"], ["Enterprise", "beta"]]), "दो, अभी सिर्फ Team और Enterprise plans पे beta में है।", ["Team", "Enterprise"], "beta"),
  B("LIMIT 3", "card", dict(icon="clock", title="Usage limit", rows=[["Counts", "plan limit में"], ["Complex", "ज़्यादा usage"]]), "तीन, लंबा या complex animation ज़्यादा usage लेता है।", ["complex", "usage"], "usage"),
  B("FIX", "versus", dict(bad="बिना content के prompt", good="अपना data / images attach"), "Best result के लिए अपना content attach करो।", ["content", "attach"], "attach"),
  cta()])
S["cm010"] = (C, "Claude Motion Complete Beginners Guide 2026", [
  B("GUIDE", "hook", dict(brand="Claude Motion", pill="GUIDE 2026", stat="30s", sub="full guide"), "Claude Motion का पूरा guide, तीस seconds में।", ["Claude", "Motion", "guide"], "guide"),
  B("WHAT", "card", dict(icon="code", title="Claude Motion", rows=[["By", "Anthropic"], ["Launch", "8 Oct 2026 (beta)"], ["Method", "code animation"]]), "Anthropic का code-based animation feature, आठ October को beta में आया।", ["Anthropic", "beta"], "beta"),
  B("START", "flow", dict(nodes=["Output → Motion", "Describe + attach", "Edit", "Export MP4"]), "Output में Motion चुनो, describe करो, edit करो, MP4 export करो।", ["Motion", "MP4"], "MP4"),
  B("BEST FOR", "list", dict(items=["Explainers", "Animated charts", "Product walkthroughs"]), "Explainers, animated charts और product walkthroughs के लिए।", ["charts", "walkthroughs"], "charts"),
  B("ACCESS", "stat", dict(value="Team+", label="Team और Enterprise plans"), "Access: Team और Enterprise plans पे।", ["Team", "Enterprise"], "Team"),
  cta()])

# ───────────────────────── ELEVENLABS v4 ─────────────────────────
E = "ELEVENLABS V4"
S["ev001"] = (E, "ElevenLabs v4 Kya Hai? Poora Breakdown", [
  B("WHAT", "hook", dict(brand="Eleven v4", pill="TEXT TO SPEECH", stat="90+", sub="languages"), "ElevenLabs v4, अब तक का सबसे emotive voice model।", ["ElevenLabs", "v4", "emotive"], "emotive"),
  B("LAUNCH", "card", dict(icon="wave", title="Eleven v4", rows=[["Launch", "28 Sep 2026"], ["Variants", "v4 + v4 Turbo"], ["Languages", "90+"]]), "अट्ठाईस September को launch, v4 और v4 Turbo के साथ।", ["v4", "Turbo"], "Turbo"),
  B("NEW", "list", dict(items=["New architecture", "Audio tags बेहतर", "Context-aware dialogue", "Better cloning"]), "New architecture, बेहतर audio tags, और scene समझकर dialogue।", ["architecture", "tags", "dialogue"], "tags"),
  B("TURBO", "stat", dict(value="~100ms", label="v4 Turbo median inference"), "Turbo की median latency लगभग सौ milliseconds, voice agents के लिए।", ["Turbo", "सौ", "milliseconds"], "Turbo"),
  B("RANK", "card", dict(icon="star", title="Benchmarks", rows=[["Artificial Analysis", "#1 (Sep 2026)"], ["Blind tests", "~75% preferred"]]), "Artificial Analysis पे number one, blind tests में करीब पचहत्तर percent पसंद।", ["number", "one"], "one"),
  cta()])
S["ev002"] = (E, "ElevenLabs v4 Voice Cloning: Apni Awaaz Clone Karo", [
  B("CLONE", "hook", dict(brand="Eleven v4", pill="VOICE CLONE", stat="10s", sub="audio से start"), "ElevenLabs v4 में voice cloning पहले से बेहतर है।", ["ElevenLabs", "cloning", "बेहतर"], "बेहतर"),
  B("IVC", "card", dict(icon="mic", title="Instant Voice Clone", rows=[["Minimum", "10 sec audio (v4)"], ["Best", "1–2 min clean audio"]]), "Blog के मुताबिक दस second से clone, पर docs best के लिए एक-दो minute clean audio बोलते हैं।", ["दस", "second", "clean"], "clean"),
  B("STEPS", "flow", dict(nodes=["Voices", "Add Voice", "Instant Clone", "Upload"]), "Voices में Add Voice, फिर Instant Voice Clone, audio upload करो।", ["Add", "Voice", "Instant"], "Instant"),
  B("QUALITY", "versus", dict(bad="Noise, echo वाली recording", good="Quiet room, एक ही speaking style"), "v4 noise भी copy करता है, इसलिए quiet room में record करो।", ["noise", "quiet"], "quiet"),
  B("PVC", "card", dict(icon="star", title="Professional Clone", rows=[["v4", "supported"], ["Best", "highest fidelity"]]), "सबसे high fidelity चाहिए तो Professional Voice Clone।", ["Professional"], "Professional"),
  cta()])
S["ev003"] = (E, "ElevenLabs v4 Kahan Milega? Free Account Se Start", [
  B("ACCESS", "hook", dict(brand="Eleven v4", pill="WHERE", stat="3", sub="places"), "ElevenLabs v4 कहाँ use कर सकते हो?", ["ElevenLabs", "v4", "कहाँ"], "कहाँ"),
  B("PRODUCTS", "list", dict(items=["ElevenCreative", "ElevenAgents", "ElevenAPI"]), "ElevenCreative, ElevenAgents और ElevenAPI, तीनों में।", ["ElevenCreative", "ElevenAgents", "ElevenAPI"], "ElevenAPI"),
  B("START", "browser", dict(url="elevenlabs.io", button="Sign up free"), "Free account बनाकर generate करना शुरू कर सकते हो।", ["Free", "account"], "Free"),
  B("MODEL", "card", dict(icon="cpu", title="Model चुनो", rows=[["Quality", "eleven_v4"], ["Real-time", "eleven_v4_turbo"]]), "Quality के लिए eleven v4, real-time के लिए v4 Turbo चुनो।", ["v4", "Turbo"], "Turbo"),
  B("PLANS", "versus", dict(bad="Limits अंदाज़े से मानो", good="Pricing page पे current plan check करो"), "Credits और plans के लिए official pricing page check करो।", ["pricing", "official"], "official"),
  cta()])
S["ev004"] = (E, "ElevenLabs v4 Audio Tags: Emotion Control Karo", [
  B("TAGS", "hook", dict(brand="Eleven v4", pill="AUDIO TAGS", stat="[ ]", sub="inline tags"), "ElevenLabs v4 में emotion control audio tags से।", ["ElevenLabs", "emotion", "tags"], "tags"),
  B("EXAMPLES", "list", dict(items=["[whispering]", "[shouting]", "[laughing]", "[light rain]"]), "जैसे whispering, shouting, laughing, या light rain जैसी sound।", ["whispering", "laughing"], "whispering"),
  B("DIRECTION", "card", dict(icon="chat", title="Natural language", rows=[["Describe", "delivery कैसी हो"], ["Accent", "भी बता सकते हो"]]), "Natural language में भी बताओ, delivery कैसी चाहिए।", ["Natural", "delivery"], "delivery"),
  B("SETTINGS", "versus", dict(bad="v4 में Style, Speed sliders", good="v4: सिर्फ Stability + Similarity"), "v4 में सिर्फ Stability और Similarity हैं, Style और Speed slider नहीं।", ["Stability", "Similarity"], "Stability"),
  B("STABILITY", "card", dict(icon="wave", title="Stability", rows=[["Low", "ज़्यादा expressive"], ["High", "ज़्यादा consistent"]]), "Stability कम मतलब ज़्यादा expressive, ज़्यादा मतलब consistent।", ["expressive", "consistent"], "expressive"),
  cta()])
S["ev005"] = (E, "ElevenLabs v4 Se Long Audio: Audiobook Aur Narration", [
  B("LONG FORM", "hook", dict(brand="Eleven v4", pill="LONG FORM", stat="1", sub="consistent voice"), "ElevenLabs v4 से लंबा audio, एक जैसी awaaz में।", ["ElevenLabs", "लंबा", "audio"], "लंबा"),
  B("STITCHING", "card", dict(icon="book", title="Request stitching", rows=[["v4", "ज़्यादा reliable"], ["Use", "Studio, Reader app"]]), "v4 में request stitching ज़्यादा reliable है, Studio और Reader app में।", ["stitching", "reliable"], "stitching"),
  B("IDENTITY", "versus", dict(bad="लंबे text में voice बदल जाए", good="v4: identity consistent रहती है"), "लंबे text में भी voice की identity same रहती है।", ["identity", "same"], "identity"),
  B("USES", "list", dict(items=["Audiobooks", "Course narration", "Character voices", "YouTube voice over"]), "Audiobooks, course narration, character voices के लिए।", ["Audiobooks", "narration"], "Audiobooks"),
  B("MODEL", "stat", dict(value="v4", label="quality के लिए eleven_v4"), "लंबे content के लिए Turbo नहीं, eleven v4 चुनो।", ["v4"], "v4"),
  cta()])
S["ev006"] = (E, "ElevenLabs v4 API: Developer Quick Start", [
  B("API", "hook", dict(brand="ElevenAPI", pill="DEVELOPERS", stat="3", sub="steps"), "ElevenLabs v4 API, तीन steps में।", ["ElevenLabs", "API"], "API"),
  B("KEY", "card", dict(icon="key", title="API key", rows=[["Dashboard", "Settings → API keys"], ["Store", ".env में secret"]]), "Dashboard के settings में API key बनाओ, env file में रखो।", ["API", "key"], "key"),
  B("SDK", "card", dict(icon="code", title="Install", rows=[["Python", "pip install elevenlabs"], ["JS", "npm i @elevenlabs/elevenlabs-js"]]), "Python में pip install elevenlabs।", ["pip", "install"], "install"),
  B("MODEL", "card", dict(icon="cpu", title="model_id", rows=[["Quality", "eleven_v4"], ["Agents", "eleven_v4_turbo"]]), "Model id में eleven v4 या v4 Turbo डालो।", ["eleven", "v4"], "v4"),
  B("SECURITY", "versus", dict(bad="Key code में hardcode", good="Key managed secret में"), "API key कभी code में hardcode मत करो।", ["hardcode"], "hardcode"),
  cta()])
S["ev007"] = (E, "ElevenLabs v3 vs v4: Kya Naya Aaya?", [
  B("V3 VS V4", "hook", dict(brand="Eleven v4", pill="VS V3", stat="4", sub="upgrades"), "ElevenLabs v3 versus v4, क्या नया आया?", ["v3", "v4"], "v4"),
  B("ACCURACY", "versus", dict(bad="v3: clone थोड़ा अलग", good="v4: source voice ज़्यादा faithful"), "v4 clone को source voice के ज़्यादा करीब रखता है।", ["clone", "करीब"], "करीब"),
  B("ACCENT", "card", dict(icon="globe", title="Native accent", rows=[["Same language", "accent वही"], ["Other language", "fluent, native"]]), "दूसरी language में v4 fluent native accent में बोलता है।", ["native", "accent"], "native"),
  B("SETTINGS", "card", dict(icon="wave", title="Settings", rows=[["v4", "Stability + Similarity"], ["Removed", "Style, Speed, SSML"]]), "v4 में Style, Speed और SSML नहीं है।", ["Style", "SSML"], "SSML"),
  B("ADVICE", "stat", dict(value="Test", label="अपनी voice पे v3 vs v4 compare करो"), "Docs की सलाह: अपनी voice पे दोनों compare करो।", ["compare"], "compare"),
  cta()])
S["ev008"] = (E, "ElevenLabs v4 Hindi Voice: Best Results Kaise Paayein", [
  B("HINDI", "hook", dict(brand="Eleven v4", pill="HINDI", stat="90+", sub="languages"), "ElevenLabs v4 में Hindi voice के best results ऐसे।", ["ElevenLabs", "Hindi"], "Hindi"),
  B("LANG", "card", dict(icon="globe", title="Languages", rows=[["v4", "90+ languages"], ["Hindi", "supported"]]), "v4 नब्बे plus languages support करता है।", ["नब्बे", "languages"], "languages"),
  B("ACCENT", "versus", dict(bad="English voice → Hindi में English accent", good="v4: Hindi में natural, fluent"), "English voice से भी Hindi में natural accent आता है।", ["natural", "accent"], "natural"),
  B("CLONE", "card", dict(icon="mic", title="अपनी Hindi voice", rows=[["Record", "Hindi में, clean"], ["Style", "एक ही tone"]]), "अपनी voice चाहिए तो Hindi में clean audio, एक ही tone में record करो।", ["clean", "tone"], "clean"),
  B("TAGS", "list", dict(items=["[excited]", "[whispering]", "[pause]"]), "और audio tags से emotion add करो।", ["tags", "emotion"], "emotion"),
  cta()])
S["ev009"] = (E, "ElevenLabs Voice Changer: Speech To Speech Kaise Karo", [
  B("VOICE CHANGER", "hook", dict(brand="ElevenLabs", pill="SPEECH TO SPEECH", stat="1→1", sub="voice swap"), "ElevenLabs voice changer से अपनी recording दूसरी voice में।", ["ElevenLabs", "voice", "changer"], "changer"),
  B("WHAT", "card", dict(icon="wave", title="Voice changer", rows=[["Input", "आपका audio"], ["Output", "दूसरी voice"], ["Keeps", "emotion, timing"]]), "आपका audio, दूसरी voice में, emotion और nuance वही।", ["emotion", "nuance"], "emotion"),
  B("KEEPS", "list", dict(items=["Whispers", "Laughs", "Accents", "Emotional cues"]), "Whispers, laughs, accents, सब preserve होते हैं।", ["preserve"], "preserve"),
  B("STEPS", "flow", dict(nodes=["Audio upload", "Voice चुनो", "Generate"]), "Audio upload करो, voice चुनो, generate करो।", ["upload", "generate"], "generate"),
  B("RULE", "versus", dict(bad="किसी की voice बिना permission", good="सिर्फ अपनी या licensed voices"), "बस दूसरों की voice बिना permission use मत करो।", ["permission"], "permission"),
  cta()])
S["ev010"] = (E, "ElevenLabs Dubbing: Video Ko Hindi Mein Dub Karo", [
  B("DUBBING", "hook", dict(brand="ElevenLabs", pill="DUBBING", stat="90+", sub="languages"), "ElevenLabs dubbing से video को Hindi में dub करो।", ["ElevenLabs", "dubbing", "Hindi"], "Hindi"),
  B("INPUT", "card", dict(icon="video", title="Input", rows=[["File", "video / audio upload"], ["URL", "YouTube, TikTok link"]]), "File upload करो, या YouTube का URL paste करो।", ["upload", "URL"], "URL"),
  B("FLOW", "flow", dict(nodes=["Upload", "Language चुनो", "Speaker detection", "Dub"]), "Language चुनो, AI speakers detect करके dub करता है।", ["Language", "speakers"], "speakers"),
  B("SIMILARITY", "card", dict(icon="wave", title="Speaker similarity", rows=[["Scale", "0–10"], ["Default", "7"]]), "Speaker similarity default सात पे रखो, ज़्यादातर content के लिए ठीक है।", ["similarity", "सात"], "सात"),
  B("COST", "versus", dict(bad="ज़्यादा languages बिना सोचे", good="हर language का अलग charge"), "ध्यान रहे, हर language का अलग charge लगता है।", ["charge"], "charge"),
  cta()])


# rendered before the 11 Nov 2026 rules; every new id must pass scripts/qa_rules.py
LEGACY = set(['cm001', 'cm002', 'cm003', 'cm004', 'cm005', 'cm006', 'cm007', 'cm008', 'cm009', 'cm010', 'ev001', 'ev002', 'ev003', 'ev004', 'ev005', 'ev006', 'ev007', 'ev008', 'ev009', 'ev010', 'kl001', 'kl002', 'kl003', 'kl004', 'kl005', 'kl006', 'kl007', 'kl008', 'kl009', 'kl010', 'mu001', 'mu002', 'mu003', 'mu004', 'mu005', 'mu006', 'mu007', 'mu008', 'mu009', 'mu010'])


def write(root):
    for vid, (series, title, beats) in S.items():
        d = os.path.join(root, "edit", vid); os.makedirs(d, exist_ok=True)
        spec = dict(id=vid, series=series, title=title, voice="hi-IN-MadhurNeural", rate="+8%", accent="#F2542D",
                    watermark="omilabs", music=series, beats=beats, rules="v2" if vid in LEGACY else "v3")
        json.dump(spec, open(os.path.join(d, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(S), "specs written")


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
