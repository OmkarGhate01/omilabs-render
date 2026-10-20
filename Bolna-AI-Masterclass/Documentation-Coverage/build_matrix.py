import re, csv, collections
R="/home/claude/Bolna-AI-Masterclass/"
EPS=[
(1,"Foundations","What Is Bolna AI? The Complete Beginner Overview"),
(2,"Foundations","How Voice AI Agents Work: Listen, Think, Speak and the Call Flow"),
(3,"Foundations","Bolna Agent Types: Conversation, Graph and IVR"),
(4,"Foundations","What a Bolna Call Really Costs: Pricing, Wallet and Plans"),
(5,"Foundations","Bolna vs Traditional IVR and Moving From Other Voice Platforms"),
(6,"Agent Creation","Create Your First Bolna Agent With Auto Build"),
(7,"Agent Creation","The Agent Builder Explained Tab by Tab"),
(8,"Agent Creation","Writing Professional Voice Agent Prompts"),
(9,"Agent Creation","Dynamic Variables: Personalising Every Call"),
(10,"Agent Creation","Interruptions, Silence and Endpointing (Engine Tab)"),
(11,"Agent Creation","Testing an Agent Before It Calls Real Customers"),
(12,"Graph Agents","Graph Agents 1: Nodes, Transitions and the Editor"),
(13,"Graph Agents","Graph Agents 2: Routers, Variables, Tools and Event Injection"),
(14,"Graph Agents","Graph Agents 3: Testing, Validation, Debugging and Versions"),
(15,"Speech and Models","Speech-to-Text: Choosing and Configuring a Transcriber"),
(16,"Speech and Models","Choosing and Configuring LLMs (Including Custom LLMs)"),
(17,"Speech and Models","Text-to-Speech, Voice Selection, Cloning and Importing Voices"),
(18,"Speech and Models","Multilingual Agents and Language Switching"),
(19,"Speech and Models","Latency: Reading the Metrics and Reducing Delay"),
(20,"Speech and Models","Speech-to-Speech Agents: OpenAI Realtime and Gemini Live"),
(21,"Speech and Models","Bring Your Own Provider Keys"),
(22,"Telephony","Telephony Providers: Twilio, Plivo, Exotel and Vobiz"),
(23,"Telephony","Phone Numbers and India Compliance (140/160 Series, Truecaller)"),
(24,"Telephony","Inbound Calling Agents and Caller Matching"),
(25,"Telephony","IVR Menus and DTMF Keypad Input"),
(26,"Telephony","Outbound Calling, Guardrails and Hangups"),
(27,"Telephony","Batch Calling: Campaigns From a CSV"),
(28,"Telephony","Call Statuses, Failed Calls and Auto-Retry"),
(29,"Telephony","Transferring Live Calls to Humans"),
(30,"Telephony","Bring Your Own SIP Trunk (BYOT)"),
(31,"Telephony","Web Calls: The Web Call SDK"),
(32,"APIs and Development","Bolna API Fundamentals: Auth, Pagination, Limits and Errors"),
(33,"APIs and Development","Creating and Managing Agents Through the v2 API"),
(34,"APIs and Development","Placing Calls and Reading Executions Through the API"),
(35,"APIs and Development","Webhooks and the Execution Payload"),
(36,"APIs and Development","Extractions and Dispositions: Structured Data From Calls"),
(37,"APIs and Development","Call History and the Analytics Dashboard"),
(38,"APIs and Development","The Bolna CLI and Terminal Dashboard"),
(39,"APIs and Development","MCP Server, Bolna Skills and AI-Readable Docs"),
(40,"Tools and Automation","Function Calling and Custom Functions"),
(41,"Tools and Automation","Appointment Booking With Cal.com"),
(42,"Tools and Automation","Knowledge Bases and FAQ Agents"),
(43,"Tools and Automation","Bolna With n8n"),
(44,"Tools and Automation","Bolna With Google Sheets"),
(45,"Tools and Automation","Bolna With Make.com, Zapier and viaSocket"),
(46,"Tools and Automation","Workflows (Beta), Campaigns and WhatsApp via AiSensy"),
(47,"Tools and Automation","Connecting a CRM Using Custom Functions and Webhooks"),
(48,"Production","Troubleshooting Bolna Calls"),
(49,"Production","Controlling Cost Per Call"),
(50,"Production","Security, Data Residency, Sub-Accounts and Enterprise"),
(51,"Production","Production Readiness Checklist and Deployment"),
(52,"Production","Capstone: A Complete Lead Qualification System"),
(53,"Production","What's New in Bolna (Rolling Changelog Episode)"),
(54,"Open Source","Bolna Open Source Explained: Self-Hosted Voice AI Agents (MIT)"),
(55,"Open Source","Self-Host Bolna Open Source With Docker: Twilio or Plivo Calls Locally"),
(56,"Open Source","Bolna Open Source in Python: Agents, Examples and the Agent API"),
]
RULES=[ # (regex on path, episode)
(r"^(index|introduction|get-started/choose-how-to-build|agents/overview)$",1),
(r"^(platform-concepts|concepts/call-flow|concepts/glossary)$",2),
(r"^concepts/agent-types$",3),
(r"^(pricing/(?!outbound)|get-started/what-it-costs)",4),
(r"^get-started/coming-from",5),
(r"^(agent-setup/studio|agent-templates)",6),
(r"^agent-setup/(overview|agent-tab|single-prompt-view|llm-tab|audio-tab|call-tab|copy-import-agent)$",7),
(r"^(prompting/introduction|writing-prompts)",8),
(r"^prompting/using-context$",9),
(r"^(agent-setup/engine-tab|troubleshooting/agent-interrupts)",10),
(r"^production/test-before",11),
(r"^graph-agent/(introduction|using-the-editor|managing-nodes|managing-transitions|edges-and-routing)$",12),
(r"^graph-agent/(router-nodes|static-nodes|variables|settings|tools-and-rag|event-injection)$",13),
(r"^graph-agent/(testing|validation|debugging|version-history|import-export|full-example)$",14),
(r"^graph-agent/graph-agents-vs-workflows$",46),
(r"^(speech-to-text|.*transcriber|deepgram-flux|assemblyai|gladia|soniox$|concepts/choosing-speech|customizations/(asr|capturing)|troubleshooting/agent-mishears)",15),
(r"^(language-models|openai-llm|openrouter|azure-openai|deepseek|anthropic|gemini-llm|custom$|concepts/choosing-llm|api-reference/user/(add|list|delete))",16),
(r"^(text-to-speech|aws-polly|.*-voice$|cartesia|kalpa|maya|rime|clone-voices|import-voices|concepts/choosing-text|api-reference/voice)",17),
(r"^(customizations/(supported|multilingual|language-switching|start-call|auto-switch)|quickstarts/multilingual)",18),
(r"^(concepts/latency|concepts/call-latencies)",19),
(r"^(speech-to-speech|openai-realtime|gemini-live)",20),
(r"^(providers|concepts/choosing-providers|api-reference/providers|integrations)$|^api-reference/providers",21),
(r"^(telephony-integrations|supported-telephony|concepts/choosing-telephony|twilio|plivo|exotel|vobiz)",22),
(r"^(buying-phone|obtaining-regulated|truecaller|compliance-application|api-reference/phone-numbers|api-reference/violations)",23),
(r"^(inbound/receiving|quickstarts/inbound|customizations/(identify|block)|api-reference/inbound|agent-setup/inbound-tab)",24),
(r"^inbound/(ivr|dtmf)",25),
(r"^outbound/(making-calls|calling-guardrails|hangup-calls)",26),
(r"^(outbound/batch|quickstarts/batch|api-reference/batches|cli/commands/batches)",27),
(r"^(outbound/auto-retry|post-call/list-phone|production/failures|troubleshooting/calls-fail)",28),
(r"^(tool-calling/transfer|troubleshooting/call-transfer)",29),
(r"^(sip-trunking|api-reference/sip-trunks)",30),
(r"^developer-resources/sdks",31),
(r"^(api-reference/(introduction|authentication|pagination|rate-limiting|errors|limits)|quickstarts/api|developer-resources/overview|api-reference/user)",32),
(r"^api-reference/agent/",33),
(r"^(api-reference/(calls|executions)|fetch-agent-executions)",34),
(r"^(post-call/(polling|execution-payload)|troubleshooting/webhook)",35),
(r"^(prompting/(using-extractions|testing-extractions|extraction-output)|agent-setup/analytics-tab|api-reference/(dispositions|extraction-categories)|migrating-to-extractions)",36),
(r"^(agent-setup/call-(history|analytics)|agents/monitor)",37),
(r"^cli/",38),
(r"^build-with-ai/|^(agents-md|llms-txt|mcp-|skills)",39),
(r"^tool-calling/(introduction|custom-|pre-call|web-search|fetch-date)|^agent-setup/tools-tab",40),
(r"^tool-calling/(fetch-calendar|book-calendar)",41),
(r"^(knowledge-base|api-reference/knowledgebase)",42),
(r"^tutorials/n8n",43),
(r"^tutorials/google-sheets",44),
(r"^tutorials/",45),
(r"^(workflows/|api-reference/workflow)",46),
(r"^(troubleshooting/|frequently-asked|getting-help|ask-bolna)",48),
(r"^production/control-cost",49),
(r"^(concepts/security|enterprise/|pricing/outbound-calling-concurrency|api-reference/sub-accounts)",50),
(r"^(production/readiness|agents/deploy)",51),
(r"^changelog/",53),
]
rows=[];seen=set()
for fn in ["llms.txt","voice-agents.md","api-reference.md"]:
    sec=""
    for line in open(R+"Research/raw/"+fn,encoding="utf-8"):
        h=re.match(r"^#+\s+(.*)",line)
        if h: sec=h.group(1).strip(); continue
        m=re.match(r"^\s*-\s*\[(.+?)\]\((https://www\.bolna\.ai/docs/[^)]+)\)(?::\s*(.*))?",line)
        if not m: continue
        title,url,desc=m.group(1),m.group(2),(m.group(3) or "").strip()
        if url in seen or "/_llms/" in url: continue
        seen.add(url)
        path=re.sub(r"\.md$","",url.split("/docs/")[1])
        ep=None
        for rx,e in RULES:
            if re.search(rx,path): ep=e;break
        rows.append([sec,title,url,ep])
T={e[0]:e[2] for e in EPS}
VER={1,2,3,4,6,22,32}  # pages for these eps partly read in this session
READ={"introduction","platform-concepts","concepts/call-flow","concepts/agent-types","concepts/glossary","get-started/what-it-costs","get-started/choose-how-to-build","pricing/call-pricing","agent-setup/studio","quickstarts/api","telephony-integrations"}
with open(R+"Documentation-Coverage/coverage-matrix.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["Docs section","Feature / page","Source URL","Planned episode","Episode title","Verification status","Remaining research gap"])
    for sec,title,url,ep in rows:
        path=re.sub(r"\.md$","",url.split("/docs/")[1])
        if path in READ: st,gap="Page read in full (10 Oct 2026)","Dashboard steps not yet tested hands-on"
        else: st,gap="Indexed only - page not yet read","Read page; verify in dashboard/API before scripting"
        if ep is None: st,gap="UNMAPPED","Assign to an episode"
        w.writerow([sec,title,url,ep or "",T.get(ep,""),st,gap])
cnt=collections.Counter(r[3] for r in rows)
print(len(rows),"pages; unmapped:",[r[2] for r in rows if r[3] is None])
print("episodes with zero doc pages:",[e[0] for e in EPS if cnt[e[0]]==0])
with open(R+"master-tracker.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["Episode","Module","Title","Doc pages mapped","Documentation sources","SEO status","Research status","Script status","Technical validation status","Storyboard status","Asset status","Editing status","QA status","Publishing status","Public URL"])
    for n,mod,t in EPS:
        src="See coverage-matrix.csv (filter Planned episode = %d)"%n
        if n==1: s=["Draft v1 (keywords = hypotheses)","Done from official docs","Draft v1 - full narration","Docs-checked; no live dashboard/API test","Draft v1","Title card, pipeline animation, thumbnail, intro sting rendered","Not started","Not started","Not started",""]
        else: s=["Not started","Docs indexed" if cnt[n] else "No official doc page - needs research","Not started","Not started","Not started","Not started","Not started","Not started","Not started",""]
        w.writerow([n,mod,t,cnt[n],src]+s)
