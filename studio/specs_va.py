# AI Voice Agents troubleshooting Shorts (va001..va010), Hinglish, v3 rules (problem on frame 0, no CTA, <=40 s).
# Niche-only batch (Omkar 16 Nov 2026). Every fact is from the ElevenLabs docs saved in
# ElevenLabs-Masterclass/Research/docs (eleven-agents__customization__*), fetched Oct 2026.
import json, os, sys

def B(tag, v, d, say, hl=(), chip=""):
    return dict(tag=tag, v=v, d=d, say=say, hl=list(hl), chip=chip or (hl[0] if hl else ""))

V = {}
V["va001"] = ("AI Agent Interrupts Callers? Fix Turn Eagerness", "AI agent interrupts", [
  B("PROBLEM", "hook", dict(problem="Agent beech mein bolta hai?", brand="ElevenLabs Agents", pill="FIX", stat="3", sub="turn modes"),
    "आपका AI agent caller की बात पूरी होने से पहले बोल पड़ता है?", ["AI", "agent", "पहले"]),
  B("WHY", "card", dict(icon="bolt", title="Turn eagerness", rows=[["Eager", "जल्दी बोलता है"], ["Normal", "default balance"], ["Patient", "रुक कर सुनता है"]]),
    "ये turn eagerness setting है: eager, normal या patient।", ["eagerness", "patient"]),
  B("FIX", "versus", dict(bad="Eager: caller कटता है", good="Patient: पूरा सुनकर जवाब"),
    "Caller सोच-सोच कर बोलते हैं तो patient रखो।", ["patient"]),
  B("WHERE", "flow", dict(nodes=["Agent settings", "Turn eagerness", "Patient", "Save"]),
    "Dashboard में Agent settings खोलो, patient चुनो, save करो।", ["patient", "save"]),
  B("BONUS", "card", dict(icon="clock", title="Take turn after silence", rows=[["Range", "1 से 30 seconds"], ["Casual call", "5 से 10 seconds"]]),
    "Silence के बाद turn लेने का time एक से तीस seconds तक set होता है।", ["silence", "तीस"]),
])
V["va002"] = ("AI Agent Won't Hang Up? Use the End Call Tool", "end call", [
  B("PROBLEM", "hook", dict(problem="Call khatam hi nahi hoti?", brand="ElevenLabs Agents", pill="FIX", stat="1", sub="system tool"),
    "बात खत्म, फिर भी आपका AI agent call नहीं काटता?", ["AI", "agent", "नहीं"]),
  B("WHY", "card", dict(icon="lock", title="End Call tool", rows=[["Dashboard agent", "default में on"], ["API या SDK agent", "खुद add करना पड़ता है"]]),
    "End Call tool dashboard वाले agents में default है, API वाले में खुद add करना पड़ता है।", ["End", "Call", "API"]),
  B("FIX", "list", dict(items=["Goodbye बोले तो call end", "Task पूरा हो तो end", "Prompt में condition लिखो"]),
    "Prompt में लिखो: goodbye या काम पूरा होते ही call end करो।", ["goodbye", "end"]),
  B("RESULT", "versus", dict(bad="Line पर silence, minutes waste", good="Natural goodbye, call end"),
    "इससे खाली minutes waste नहीं होते।", ["minutes", "waste"]),
])
V["va003"] = ("AI Calls Hitting Voicemail? Turn On Detection", "voicemail", [
  B("PROBLEM", "hook", dict(problem="Voicemail pe minutes waste?", brand="ElevenLabs Agents", pill="FIX", stat="1", sub="system tool"),
    "आपके AI calls voicemail पर जाकर minutes waste करते हैं?", ["AI", "voicemail", "waste"]),
  B("FIX", "card", dict(icon="check", title="Voicemail Detection", rows=[["पहचानता है", "automated greeting"], ["फिर", "message या call end"]]),
    "Voicemail Detection tool on करो, ये automated greeting पहचान लेता है।", ["Voicemail", "Detection"]),
  B("CHOOSE", "versus", dict(bad="Message छोड़ो", good="या तुरंत call end"),
    "फिर चुनो: छोटा message छोड़ो, या call तुरंत end करो।", ["message", "end"]),
  B("TRACK", "card", dict(icon="chart", title="Logs", rows=[["कहाँ", "conversation history"], ["Batch calls", "results में भी"]]),
    "हर detection conversation history और batch call results में दिखता है।", ["history", "batch"]),
])
V["va004"] = ("AI Agent Says the Wrong Name? Dynamic Variables", "dynamic variables", [
  B("PROBLEM", "hook", dict(problem="Customer ka naam galat?", brand="ElevenLabs Agents", pill="FIX", stat="{{ }}", sub="dynamic variables"),
    "आपका AI agent हर customer को एक ही नाम से बुलाता है?", ["AI", "agent", "नाम"]),
  B("WHY", "versus", dict(bad="नाम prompt में hardcoded", good="नाम हर call पर runtime से"),
    "क्योंकि नाम prompt में hardcode है। Dynamic variables use करो।", ["hardcode", "Dynamic"]),
  B("WHERE", "list", dict(items=["System prompt", "First message", "Tool parameters"]),
    "ये system prompt, first message और tools, तीनों में चलते हैं।", ["prompt", "first", "tools"]),
  B("EXAMPLE", "card", dict(icon="mobile", title="First message", rows=[["लिखो", "Hi {{customer_name}}"], ["Call पर", "Hi Rahul"]]),
    "First message में customer name का variable डालो, हर call अपना नाम लेगी।", ["variable", "नाम"]),
])
V["va005"] = ("AI Agent Mispronounces Names? Fix in 2 Minutes", "mispronounces", [
  B("PROBLEM", "hook", dict(problem="Brand name galat bolta hai?", brand="ElevenLabs Agents", pill="FIX", stat="1", sub="dictionary"),
    "आपका AI agent brand या शहर का नाम गलत बोलता है?", ["AI", "agent", "गलत"]),
  B("FIX", "card", dict(icon="book", title="Pronunciation dictionary", rows=[["कहाँ", "Voice settings"], ["क्या", "नाम, जगह, technical words"]]),
    "Voice settings में pronunciation dictionary add करो।", ["pronunciation", "dictionary"]),
  B("MODEL", "versus", dict(bad="Phoneme tags हर model में नहीं", good="v4, v3, Flash v2 में चलते हैं"),
    "Phoneme tags सिर्फ v4, v3 और Flash v2 models में चलते हैं।", ["v4", "v3", "Flash"]),
  B("ELSE", "card", dict(icon="check", title="बाकी models", rows=[["Use", "alias tags"], ["मतलब", "spelling बदलकर लिखो"]]),
    "बाकी models में alias tags से spelling बदलकर सही आवाज़ लो।", ["alias", "spelling"]),
])
V["va006"] = ("AI Agent Talks Too Fast? Set the Speed Right", "talks too fast", [
  B("PROBLEM", "hook", dict(problem="Agent bahut fast bolta hai?", brand="ElevenLabs Agents", pill="FIX", stat="0.7–1.2", sub="speed range"),
    "आपका AI agent इतना fast बोलता है कि customer समझ नहीं पाता?", ["AI", "fast", "समझ"]),
  B("FIX", "stat", dict(value="1.0", label="Default speed, range 0.7 से 1.2"),
    "Speed setting default एक है, range zero point seven से one point two।", ["Speed", "range"]),
  B("WHEN", "versus", dict(bad="Fast: support calls में confusion", good="Slow: explain वाले calls साफ"),
    "Explain वाले calls में speed थोड़ी कम रखो।", ["speed", "कम"]),
  B("WHERE", "flow", dict(nodes=["Agent", "Voice tab", "Speed", "Save"]),
    "Voice tab में speed बदलो और save करो।", ["Voice", "save"]),
])
V["va007"] = ("AI Agent Stuck in English? Language Detection", "language detection", [
  B("PROBLEM", "hook", dict(problem="Hindi bolo, English mein jawab?", brand="ElevenLabs Agents", pill="FIX", stat="2", sub="switch triggers"),
    "Customer Hindi बोलता है, पर AI agent English में ही जवाब देता है?", ["Hindi", "English", "agent"]),
  B("WHY", "card", dict(icon="lock", title="Language detection", rows=[["Default", "on नहीं होता"], ["Fix", "system tool enable करो"]]),
    "Language detection tool अपने आप on नहीं होता, खुद enable करो।", ["detection", "enable"]),
  B("HOW", "list", dict(items=["Caller दूसरी language में बोले", "या language बदलने को बोले"]),
    "ये दो case में switch करता है: caller दूसरी भाषा बोले, या बदलने को कहे।", ["switch", "भाषा"]),
  B("TIP", "card", dict(icon="check", title="ElevenLabs tip", rows=[["सारी languages", "enable करो"], ["साथ में", "detection tool"]]),
    "Docs की सलाह: सारी languages enable करो, साथ में ये tool।", ["languages", "tool"]),
])
V["va008"] = ("AI Agent Can't Reach a Human? Transfer the Call", "transfer the call", [
  B("PROBLEM", "hook", dict(problem="Angry caller, koi human nahi?", brand="ElevenLabs Agents", pill="FIX", stat="3", sub="transfer types"),
    "Caller गुस्से में है, और AI agent उसे किसी human तक नहीं पहुँचा पाता?", ["AI", "agent", "human"]),
  B("FIX", "card", dict(icon="mobile", title="Transfer to number", rows=[["Kahan", "phone number या SIP"], ["Via", "Twilio, SIP trunk"]]),
    "Transfer to number tool से call phone number या SIP पर जाती है।", ["Transfer", "number"]),
  B("TYPES", "list", dict(items=["Conference transfer (default)", "Blind transfer", "SIP REFER"]),
    "Default conference transfer है, जिसमें agent निकल जाता है और caller human से बात करता है।", ["conference", "human"]),
  B("NOTE", "versus", dict(bad="Chat widget में नहीं चलता", good="सिर्फ phone calls में"),
    "ध्यान रखो, ये सिर्फ phone calls में चलता है, chat widget में नहीं।", ["phone", "widget"]),
])
V["va009"] = ("Awkward Silence on AI Calls? Use Soft Timeout", "soft timeout", [
  B("PROBLEM", "hook", dict(problem="Call pe awkward silence?", brand="ElevenLabs Agents", pill="FIX", stat="Hmm...", sub="filler phrase"),
    "जवाब सोचते वक्त AI agent चुप हो जाता है, और caller सोचता है call कट गई?", ["चुप", "call", "कट"]),
  B("FIX", "card", dict(icon="clock", title="Soft timeout", rows=[["बोलता है", "Hmm... एक second"], ["Default", "off रहता है"]]),
    "Soft timeout on करो। Agent hmm या let me think बोलेगा।", ["Soft", "timeout"]),
  B("WHY", "versus", dict(bad="Silence: caller hang up", good="Filler: बात natural लगती है"),
    "इससे बातचीत natural लगती है।", ["natural"]),
  B("SET", "flow", dict(nodes=["Agent settings", "Soft timeout", "Seconds set", "Save"]),
    "Seconds set करो, उसके बाद filler बोलेगा।", ["Seconds", "filler"]),
])
V["va010"] = ("AI Calls Running Forever? Set Max Duration", "max duration", [
  B("PROBLEM", "hook", dict(problem="Ek call 30 min chal gayi?", brand="ElevenLabs Agents", pill="FIX", stat="600s", sub="default limit"),
    "आपकी एक AI call आधे घंटे चल गई, और बिल बढ़ गया?", ["AI", "call", "बिल"]),
  B("FIX", "stat", dict(value="10 min", label="Default max conversation duration"),
    "Max conversation duration default दस minute है।", ["Max", "दस"]),
  B("RANGE", "card", dict(icon="clock", title="Set your limit", rows=[["Minimum", "60 seconds"], ["Maximum", "7,200 seconds"]]),
    "आप इसे साठ seconds से दो घंटे तक set कर सकते हो।", ["साठ", "घंटे"]),
  B("TIP", "versus", dict(bad="Limit नहीं: खर्चा control नहीं", good="Limit सही: minutes बचें"),
    "Use case के हिसाब से limit रखो, minutes बचेंगे।", ["limit", "minutes"]),
])


def write(out):
    for k, (title, kw, beats) in V.items():
        spec = dict(id=k, series="AI VOICE AGENTS", title=title, search_kw=kw, voice="hi-IN-MadhurNeural", rate="+8%",
                    accent="#2D7FF9", watermark="omilabs", music="ELEVENLABS V4", rules="v3", beats=beats)
        d = os.path.join(out, k); os.makedirs(d, exist_ok=True)
        json.dump(spec, open(os.path.join(d, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", len(V))


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else "edit")
