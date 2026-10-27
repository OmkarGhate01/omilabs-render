# ElevenLabs v4 Shorts — 10 Shorts, vidIQ: "elevenlabs v4" +3007%, "elevenlabs voice cloning" 33k/mo
# Standalone series (no episode dependency). Affiliate: https://try.elevenlabs.io/c9bnghlu9434
# Disclosure: affiliate link in description — "I may earn a commission at no extra cost to you"
# Omkar's ElevenLabs voice: https://elevenlabs.io/app/voice-lab/share/0ca97729faff22ee3841f4eb985cd7e58e4a7687ba6d4afde460babdf249999d/8WqHCYyrnUqoK70Px5EJ
AFFIL = "https://try.elevenlabs.io/c9bnghlu9434"
VOICE = "https://elevenlabs.io/app/voice-lab/share/0ca97729faff22ee3841f4eb985cd7e58e4a7687ba6d4afde460babdf249999d/8WqHCYyrnUqoK70Px5EJ"
CTA = "Save this — aur ElevenLabs v4 free mein try karo."

SHORTS = [
    dict(id="ev001", ep=None, series="el_v4", accent="violet",
         title="ElevenLabs v4 Kya Hai? 60 Seconds Mein Poora Breakdown",
         topic="elevenlabs v4 new features overview",
         tags=["elevenlabs v4", "elevenlabs", "elevenlabs 2026", "elevenlabs new features", "ai voice", "text to speech"],
         beats=[
             dict(v="hook", d=dict(lines=["ElevenLabs v4 —", "kya badla?", "60 sec mein."]), say="ElevenLabs v4 aaya hai — kya naya hai? 60 seconds mein sab jaano."),
             dict(k="new in v4", v="list", d=dict(items=["Voice cloning next level", "Emotional control", "Multilingual v2 faster", "Projects: long-form audio"]), say="Voice cloning next level, emotional control, faster multilingual aur Projects feature."),
             dict(k="emotional control", v="versus", d=dict(bad="v3: ek hi tone, flat delivery", good="v4: sad, excited, whisper — sab control mein"), say="V3 mein tone flat thi. V4 mein sad, excited, whisper — sab control kar sakte ho."),
             dict(k="speed", v="stat", d=dict(value="2x", label="faster than ElevenLabs v2 Multilingual", ring=0.85), say="Multilingual v2 se do guna fast hai v4 ka generation."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),

    dict(id="ev002", ep=None, series="el_v4", accent="cyan",
         title="ElevenLabs Voice Cloning: 1 Min Mein Apni Awaaz Clone Karo",
         topic="how to clone your voice with elevenlabs",
         tags=["elevenlabs voice cloning", "elevenlabs v4", "voice clone ai", "ai voice clone", "elevenlabs tutorial", "clone voice"],
         beats=[
             dict(v="hook", d=dict(lines=["Apni awaaz clone", "karo — sirf", "1 minute mein."]), say="ElevenLabs mein apni awaaz clone karna sirf 1 minute ka kaam hai."),
             dict(k="step 1", v="orb", d=dict(label="Voices → Add Voice → Clone"), say="ElevenLabs dashboard mein Voices → Add Voice → Instant Voice Clone click karo."),
             dict(k="step 2", v="card", d=dict(icon="mic", title="Sample Record Karo", rows=[["Duration", "1-5 min best"], ["Quality", "quiet room, no echo"], ["Language", "jo bhi bolna ho"]], hl=0), say="1 se 5 minute ka clean audio sample do — quiet room mein record karo."),
             dict(k="result", v="card", d=dict(icon="wave", title="Cloned Voice", rows=[["Accuracy", "very high"], ["Languages", "29+ supported"], ["Use it", "Text to Speech mein"]]), say="Clone hone ke baad ye voice 29 plus languages mein text-to-speech ke liye ready hai."),
             dict(k="tip", v="versus", d=dict(bad="Noisy recording — artifacts aate hain", good="Clean quiet recording — near-perfect clone"), say="Noisy recording se artifacts aate hain. Clean recording se near-perfect clone milta hai."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),

    dict(id="ev003", ep=None, series="el_v4", accent="green",
         title="ElevenLabs Free Plan Mein Kya Milta Hai? (2026)",
         topic="elevenlabs free plan features and limits 2026",
         tags=["elevenlabs free", "elevenlabs v4", "elevenlabs free plan", "free text to speech", "elevenlabs tutorial", "ai voice free"],
         beats=[
             dict(v="hook", d=dict(lines=["ElevenLabs free mein", "kya milta hai?", "Dekho."]), say="ElevenLabs ka free plan mein exactly kya milta hai? Seedha baat karte hain."),
             dict(k="free plan", v="card", d=dict(icon="wallet", title="Free Plan (2026)", rows=[["Credits", "10,000/month"], ["Voices", "3 custom"], ["Projects", "limited"], ["Commercial use", "no"]]), say="Free plan mein 10,000 credits per month, 3 custom voices, limited Projects — aur commercial use nahi."),
             dict(k="credits explained", v="stat", d=dict(value=10000, label="characters per month on free plan", ring=0.6), say="10,000 characters per month — ek 1000-word blog post ke liye kaafi hai."),
             dict(k="upgrade why", v="versus", d=dict(bad="Free: no commercial use, limited voices", good="Starter ($5/mo): 30k chars, commercial, more voices"), say="Commercial use chahiye? Starter plan sirf 5 dollar per month mein milta hai."),
             dict(k="my voice", v="card", d=dict(icon="star", title="Omkar Ka Voice", rows=[["Try karo", "link description mein"], ["Free mein", "sun sakte ho"]]), say="Mere khud ke AI voice ka link description mein hai — free mein sun sakte ho."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),

    dict(id="ev004", ep=None, series="el_v4", accent="amber",
         title="ElevenLabs Emotional Voice: Sad, Happy, Whisper Control Karo",
         topic="elevenlabs v4 emotional voice control and style settings",
         tags=["elevenlabs v4", "elevenlabs emotional", "ai voice emotion", "elevenlabs style", "elevenlabs tutorial", "text to speech emotion"],
         beats=[
             dict(v="hook", d=dict(lines=["AI voice mein", "emotion control —", "ye dekho."], hot=1), say="ElevenLabs v4 mein AI voice mein emotion control possible hai."),
             dict(k="settings", v="card", d=dict(icon="wave", title="Emotion Controls", rows=[["Stability", "0 = expressive, 1 = flat"], ["Similarity Boost", "original voice kitni close"], ["Style", "0 = natural, 1 = exaggerated"]]), say="Teen sliders hain: Stability, Similarity Boost aur Style."),
             dict(k="sad voice", v="card", d=dict(icon="chat", title="Sad/Soft ke liye", rows=[["Stability", "0.3 (low)"], ["Style", "0.2"], ["Result", "soft, slower delivery"]]), say="Sad ya soft voice ke liye Stability 0.3 aur Style 0.2 rakhna."),
             dict(k="excited voice", v="card", d=dict(icon="bolt", title="Excited ke liye", rows=[["Stability", "0.6"], ["Style", "0.8 (high)"], ["Result", "energetic, fast"]]), say="Excited voice ke liye Stability 0.6 aur Style 0.8 rakhna."),
             dict(k="experiment", v="orb", d=dict(label="Text change bhi karo — '!' se energy badhti hai"), say="Tip: text mein exclamation mark lagao — AI naturally zyada energy add karta hai."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),

    dict(id="ev005", ep=None, series="el_v4", accent="violet",
         title="ElevenLabs Projects: Long Audio Book Banana — Complete Guide",
         topic="elevenlabs projects feature for long form audio generation",
         tags=["elevenlabs projects", "elevenlabs v4", "elevenlabs audiobook", "long form tts", "elevenlabs tutorial", "ai audiobook"],
         beats=[
             dict(v="hook", d=dict(lines=["ElevenLabs mein", "puri book ka audio", "ek click mein."]), say="ElevenLabs Projects se puri book ka audio ek hi flow mein generate hota hai."),
             dict(k="what is projects", v="card", d=dict(icon="book", title="Projects Feature", rows=[["Long form", "chapter by chapter"], ["Multiple voices", "different characters"], ["Export", "MP3 / WAV"]]), say="Projects feature mein chapters alag kar sakte ho, alag voices assign karo, phir export karo."),
             dict(k="how to start", v="flow", d=dict(nodes=["Text paste karo", "Chapters set karo", "Voices assign karo", "Generate"]), say="Text paste karo, chapters set karo, voices assign karo, generate — bas itna hi kaam hai."),
             dict(k="use case", v="list", d=dict(items=["Audiobook creation", "Long podcast script", "Course narration", "YouTube voice over"]), say="Audiobook, podcast, course narration, YouTube voice over — sab ke liye perfect hai."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),

    dict(id="ev006", ep=None, series="el_v4", accent="green",
         title="ElevenLabs API Se Text to Speech: Developer Guide",
         topic="elevenlabs api integration for developers",
         tags=["elevenlabs api", "elevenlabs v4", "elevenlabs developer", "text to speech api", "elevenlabs tutorial", "ai voice api"],
         beats=[
             dict(v="hook", d=dict(lines=["ElevenLabs API —", "developer ke liye", "5 min guide."]), say="ElevenLabs API integrate karna sirf 5 minutes ka kaam hai."),
             dict(k="api key", v="card", d=dict(icon="key", title="API Key", rows=[["Get it", "Settings → API Keys"], ["Free plan", "bhi kaam karta hai"], ["Header", "xi-api-key: <key>"]]), say="Settings mein jao, API Keys section mein key generate karo — free plan mein bhi kaam karta hai."),
             dict(k="endpoint", v="card", d=dict(icon="code", title="Basic TTS Call", rows=[["POST", "/v1/text-to-speech/{voice_id}"], ["Body", '{"text": "...", "model_id": "eleven_multilingual_v2"}'], ["Returns", "audio/mpeg stream"]]), say="POST request bhejo, text aur model_id body mein dalo, audio stream return aata hai."),
             dict(k="python example", v="card", d=dict(icon="code", title="Python — 4 lines", rows=[["import", "elevenlabs"], ["client", "ElevenLabs(api_key=...)"], ["audio", "client.generate(text=..., voice=...)"], ["save(audio)", '"output.mp3"']]), say="Python mein sirf 4 lines: import, client banao, generate karo, save karo."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),

    dict(id="ev007", ep=None, series="el_v4", accent="cyan",
         title="ElevenLabs vs ElevenLabs v4: Kya Naya Aya?",
         topic="elevenlabs v4 vs previous version comparison",
         tags=["elevenlabs v4", "elevenlabs comparison", "elevenlabs new", "ai voice update", "elevenlabs 2026", "text to speech comparison"],
         beats=[
             dict(v="hook", d=dict(lines=["v3 tha achi.", "v4 mein kya", "naya aya?"], hot=1), say="V3 bhi achi thi. Lekin V4 mein kya genuinely better hai?"),
             dict(k="voice quality", v="versus", d=dict(bad="v3: thoda robotic at low stability", good="v4: human-like even at low stability"), say="V3 low stability pe thoda robotic tha. V4 low stability pe bhi human-like hai."),
             dict(k="multilingual", v="card", d=dict(icon="globe", title="Multilingual v2 → v4", rows=[["Speed", "2x faster"], ["Languages", "29 → 32+"], ["Hindi", "much better"]]), say="Multilingual 2x fast hai, 32 plus languages, aur Hindi ka quality significantly better hai."),
             dict(k="cloning", v="card", d=dict(icon="mic", title="Voice Cloning v4", rows=[["Sample needed", "1 min (v3: 3 min)"], ["Accuracy", "higher"], ["Languages", "cross-lingual cloning"]]), say="Cloning ke liye V4 mein 1 minute ka sample kaafi hai — V3 mein 3 minute chahiye the."),
             dict(k="verdict", v="orb", d=dict(label="v4 = clear upgrade for Hindi + multilingual content"), say="Hindi aur multilingual content ke liye V4 clear upgrade hai."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),

    dict(id="ev008", ep=None, series="el_v4", accent="amber",
         title="ElevenLabs Hindi Voice: Best Settings Kya Hain?",
         topic="elevenlabs hindi text to speech best voice and settings",
         tags=["elevenlabs hindi", "elevenlabs v4", "hindi text to speech", "hindi ai voice", "elevenlabs tutorial", "ai hindi voice"],
         beats=[
             dict(v="hook", d=dict(lines=["ElevenLabs mein", "Hindi voice", "kaise best karo?"], hot=1), say="ElevenLabs mein Hindi ke liye best voice aur settings kya hain? Let's see."),
             dict(k="best model", v="card", d=dict(icon="cpu", title="Model Choose Karo", rows=[["eleven_multilingual_v2", "best for Hindi"], ["eleven_turbo_v2_5", "fast, good Hindi"], ["eleven_v4", "latest, top quality"]]), say="Hindi ke liye eleven multilingual v2 best hai — v4 bhi excellent hai."),
             dict(k="settings", v="card", d=dict(icon="wave", title="Hindi Best Settings", rows=[["Stability", "0.5-0.7"], ["Similarity Boost", "0.7-0.8"], ["Style", "0.3-0.5"]]), say="Stability 0.5 se 0.7, Similarity Boost 0.7 se 0.8, Style 0.3 se 0.5 rakhna."),
             dict(k="voice pick", v="list", d=dict(items=["Premade voices mein 'Matilda' ya 'Aria' try karo", "Custom clone: apni Hindi awaaz upload karo", "Omkar ka voice (link in description)"]), say="Premade voices mein Matilda ya Aria try karo, ya apni Hindi awaaz clone karo."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),

    dict(id="ev009", ep=None, series="el_v4", accent="violet",
         title="ElevenLabs Speech to Speech: Voice Swap Kaise Karo",
         topic="elevenlabs speech to speech voice conversion feature",
         tags=["elevenlabs speech to speech", "elevenlabs v4", "voice conversion ai", "elevenlabs features", "ai voice swap", "elevenlabs tutorial"],
         beats=[
             dict(v="hook", d=dict(lines=["Ek voice record karo,", "doosri voice mein", "sunao — ElevenLabs."]), say="Ek voice record karo — ElevenLabs use mein convert karke doosri voice mein sunao."),
             dict(k="what it is", v="card", d=dict(icon="wave", title="Speech to Speech", rows=[["Input", "tumhara audio"], ["Output", "kisi aur ki awaaz mein"], ["Tone/pace", "original hi rehti hai"]]), say="Tumhara audio input, output kisi aur ki cloned voice mein aata hai. Lekin tone aur pace teri hi rehti hai."),
             dict(k="use cases", v="list", d=dict(items=["Dubbing: video apni awaaz mein dub karo", "AI avatar: consistent persona ke liye", "Content localization: different voices same script"]), say="Dubbing, AI avatar, content localization — sab ke liye use ho sakta hai."),
             dict(k="how to use", v="flow", d=dict(nodes=["Apna audio upload karo", "Target voice select karo", "Convert click karo", "Download karo"]), say="Apna audio upload karo, target voice choose karo, convert click karo, download karo."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),

    dict(id="ev010", ep=None, series="el_v4", accent="green",
         title="ElevenLabs Dubbing Studio: Video Ko Hindi Mein Dub Karo",
         topic="elevenlabs dubbing studio for video localization",
         tags=["elevenlabs dubbing", "elevenlabs v4", "video dubbing ai", "hindi dubbing ai", "elevenlabs tutorial", "ai video dubbing"],
         beats=[
             dict(v="hook", d=dict(lines=["YouTube video", "Hindi mein dub karo —", "AI se."]), say="Koi bhi YouTube video Hindi ya kisi bhi language mein AI se dub kar sakte ho."),
             dict(k="dubbing studio", v="card", d=dict(icon="video", title="ElevenLabs Dubbing", rows=[["Input", "video URL ya file"], ["Output", "dubbed video"], ["Languages", "29+ supported"]]), say="Dubbing Studio mein video URL ya file do — 29 plus languages mein dubbed video milti hai."),
             dict(k="how it works", v="flow", d=dict(nodes=["Video upload", "Target language choose", "Speaker detection", "Dub + sync"]), say="Video upload karo, language choose karo, AI speakers detect karta hai, dub karta hai aur lip sync karta hai."),
             dict(k="quality", v="versus", d=dict(bad="Manual dubbing: expensive, slow, weeks lgte hain", good="ElevenLabs: minutes mein, much cheaper"), say="Manual dubbing weeks leti hai aur costly hai. ElevenLabs minutes mein karta hai."),
             dict(k="", v="cta", d=dict(title="Save this"), say=CTA),
         ]),
]
