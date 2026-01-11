# PyAgent Improvement Research & Roadmap

## 🚀 Ongoing Research
- **GLM-4.7 Cost Efficiency**: Benchmarking sub-7 cent per million token coding performance.
- **Latent Reasoning Consistency**: Probing hidden English-centered reasoning in multilingual agents.
- **Hopper Matmul Optimization**: Exploring SOTA GPU kernel design for local model inference.

## ✅ Completed Research
| Research Paper / Concept | Status | Implementation Detail |
| :--- | :--- | :--- |
| **Digital Red Queen (Sakana AI)** | ✅ Implemented | Red Queen Benchmark tests for adversarial evolution. |
| **Confucius Code Agent (Meta)** | ✅ Implemented | Hierarchical working memory and persistent scratchpads. |
| **Prompt Caching (ngrok)** | ✅ Implemented | Prefix-based hash caching in ResponseCache. |
| **Byzantine Consensus (Phase 129)** | ✅ Implemented | Orchestrator integration with ByzantineConsensusAgent. |
| **Self-Verification (Keio 2026)** | ✅ Implemented | Added BaseAgent.verify_self() hook. |

"Physics of AI" 
Learning sparse attention has a sticky plateau, representation collapse, and branching dynamics
https://kindxiaoming.github.io/blog/2026/sparse-attention-2/

if reasoning trained LLMs solve problems across languages, and finds their hidden reasoning is English centered.
Multilingual answers can look fine, yet silent reasoning is much weaker in languages with less training data.
They make the model solve the same math problems in 11 languages, then hide most written steps and ask for the final answer.
If it stays correct when the answer is not yet written, they call that latent reasoning, meaning the solution already exists inside the model.
On easier grade school math, bigger models and common training languages like English or Chinese can stay correct even when 0% of the written reasoning is shown.
But languages with less training data, like Swahili and Telugu, show a weaker early signal and lean more on long written explanations.
On harder contest style problems that early signal mostly vanishes, yet the model's internal states, the hidden signals inside it, move in similar patterns across languages and often look most like English.
This matters because a model can sound fluent in many languages while its silent reasoning strength varies, so checking only the final answer or the written steps can hide weaknesses.
https://arxiv.org/abs/2601.02996

Brilliant post on prompt caching. 🤯
One of the most effective yet underutilized techniques for cutting LLM usage costs without sacrificing performance.  
If you’re building with LLMs at scale, this is a must-know optimization. 
https://ngrok.com/blog/prompt-caching

Z AI Just Dropped GLM-4.7 - And It Might Be the Coding Model You Didn’t Know You Needed
Your next AI coding assistant could cost one-seventh of what you’re paying now. Here’s why that matters.
TLDR/ADHD Summary
- Z AI released GLM-4.7, a new AI model that’s really good at coding, reasoning, and running complex multi-step workflows. 
- You can use it through their website, API, or download it free to run yourself. 
- The big deal: it claims Claude-level coding performance at roughly one-seventh the cost. 
- Works with popular coding tools already. 
- If you’re building anything with AI and watching your budget, this is worth testing.
---
The AI model wars just got more interesting. Z ai has released GLM-4.7, their latest flagship large language model, and it’s making some bold claims: frontier-level performance on coding and reasoning benchmarks, open weights for anyone to download, and pricing that makes Claude and GPT look expensive by comparison.
For entrepreneurs and business leaders trying to stay ahead of the AI curve without emptying their budgets, this one deserves your attention.
---
What Makes GLM-4.7 Different
Let’s cut through the technical jargon. GLM-4.7 is built for three things that matter to anyone running a business:
Coding that actually works. The model shows significant improvements on real-world coding benchmarks like LiveCodeBench and SWE-bench. Translation: it’s better at writing, refactoring, and understanding code across multiple files and entire projects—not just isolated snippets.
Reasoning that goes deeper. Higher scores on logic, math, and problem-solving tests mean this model can handle the kind of complex, multi-step thinking that separates useful AI from frustrating AI.
Agent workflows that stay on track. This is where things get interesting for automation enthusiasts. GLM-4.7 includes “thinking modes” that let the model explicitly reason between actions, maintaining context across long, multi-turn tasks. If you’ve ever watched an AI lose the plot halfway through a complex workflow, you know why this matters.
---
The Access Story: Open, Affordable, and Flexible
Here’s where GLM-4.7 stands apart from the crowd:
Browser-based chat: Use it directly at Z AI's website, similar to ChatGPT or Claude. Sign in, start chatting, done.
API access: Developers can call the model through Z AI's API at roughly $0.60 per million input tokens and $2.20 per million output tokens. For context, that’s significantly cheaper than premium models from OpenAI or Anthropic.
Third-party platforms: Access it through OpenRouter, Kilo Code, and other routing services that let you switch between models easily.
Self-hosting: Download the open weights from Hugging Face and run it on your own hardware. Guides from Unsloth and others make local deployment surprisingly approachable.
Coding tool integrations: GLM-4.7 already works inside popular coding assistants like Claude Code, Kilo Code, Roo Code, and Cline. Just select it from the model menu.
---
The Price That Makes You Look Twice
Z AI is advertising a “GLM Coding Plan” that promises Claude-level coding performance at approximately one-seventh the cost, with higher usage quotas aimed at developers and teams running heavy AI workloads.
For solo entrepreneurs bootstrapping their tech stack, or small teams trying to build AI-powered tools without venture capital budgets, that math changes everything.
---
The Bigger Picture
GLM-4.7 represents a broader shift in the AI landscape: frontier-level capabilities are no longer locked behind the gates of a few massive tech companies. Open models with serious performance are becoming the norm, and that’s excellent news for anyone who wants to leverage AI without becoming dependent on a single provider.
The 200K token context window means you can feed it entire codebases, long research documents, or multi-week conversation histories. The thinking modes mean your AI agents might actually finish complex tasks without derailing.
Will GLM-4.7 dethrone Claude or GPT-4 for every use case? Probably not. But it doesn’t need to. It just needs to be good enough—and cheap enough—to make you reconsider your current AI budget.
---
What This Means For You
If you’re building automations, coding assistants, or AI-powered tools, GLM-4.7 gives you another serious option in your toolkit. The open weights mean you’re not locked in. The pricing means you can experiment more freely. The performance benchmarks suggest you won’t be sacrificing quality for cost.
That’s the kind of competitive pressure that benefits everyone who uses AI.
---
🧪 The AI Experiment
You’ve just experienced something different. This article was researched, analyzed, and written by Helaina - an AI-powered news reporter covering the rapidly evolving world of artificial intelligence.
This isn’t about replacing human journalism. It’s about demonstrating what’s possible when AI tools are applied thoughtfully to real-world information gathering and storytelling.
The technology powering this report is real. The news is real. The experiment is ongoing.
Stay curious, stay informed, and remember: understanding AI isn’t just about keeping up - it’s about getting ahead.
---
This news article is possible due to the support from our sponsor, Everyday AI Vibe Magazine!

Learning Latent Action World Models In The Wild (FAIR at Meta, INRIA & NYU, January 2026) 
Paper: [https://arxiv.org/abs/2601.05230](https://arxiv.org/abs/2601.05230) 
Abstract:
"Agents capable of reasoning and planning in the real world require the ability of predicting the consequences of their actions. While world models possess this capability, they most often require action labels, that can be complex to obtain at scale. This motivates the learning of latent action models, that can learn an action space from videos alone. Our work addresses the problem of learning latent actions world models on in-the-wild videos, expanding the scope of existing works that focus on simple robotics simulations, video games, or manipulation data. While this allows us to capture richer actions, it also introduces challenges stemming from the video diversity, such as environmental noise, or the lack of a common embodiment across videos. To address some of the challenges, we discuss properties that actions should follow as well as relevant architectural choices and evaluations. We find that continuous, but constrained, latent actions are able to capture the complexity of actions from in-the-wild videos, something that the common vector quantization does not. We for example find that changes in the environment coming from agents, such as humans entering the room, can be transferred across videos. This highlights the capability of learning actions that are specific to in-the-wild videos. In the absence of a common embodiment across videos, we are mainly able to learn latent actions that become localized in space, relative to the camera. Nonetheless, we are able to train a controller that maps known actions to latent ones, allowing us to use latent actions as a universal interface and solve planning tasks with our world model with similar performance as action-conditioned baselines. Our analyses and experiments provide a step towards scaling latent action models to the real world."

https://www.clcoding.com/2023/10/regular-expressions-in-python.html?fbclid=IwY2xjawPQG3FleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHkEiU3u3iY1zfW6qSQ-OtcQRlpSs-rl2nD9czonI1ZzQJW0ymB3150tvUvLc_aem_lEtwvQpP6u76iZL7Gpj6_g

Meta and Harvard Researchers Introduce the Confucius Code Agent (CCA): A Software Engineering Agent that can Operate at Large-Scale Codebases
Confucius Code Agent from Meta and Harvard shows how much performance on real world software tasks comes from scaffolding rather than model size. Built on the Confucius SDK, it combines hierarchical working memory, persistent note taking, modular tools and a meta agent driven build, test, improve loop to reach 52.7 Resolve@1 on SWE Bench Pro with Claude 4.5 Sonnet, surpassing Opus based baselines......
Full analysis: https://www.marktechpost.com/.../meta-and-harvard.../
Paper: https://arxiv.org/pdf/2512.10398

🚀 DeepSeek V4: What’s the Buzz?
DeepSeek — the Chinese AI startup that startled Silicon Valley with its earlier models — is reportedly gearing up to unveil its next-generation flagship, *V4*, around the Lunar New Year (mid-February). This launch is generating buzz because insiders say V4 could redefine expectations for AI coding models. 
 🧠 Coding at the Core
Unlike some models that balance general language tasks with code, V4 reportedly leans hard into *software engineering and development*. Early *internal benchmarks* suggest it could outperform major competitors like Anthropic’s Claude and OpenAI’s GPT series on coding tasks — a remarkable claim if verified.
https://cybernews.com/ai-news/chinas-deepseek-rival-openai-coding/?fbclid=IwY2xjawPQG91leHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHoKYsz0SQmDHKh-3LYAFkmHD6c-5PM1dbV39kx-wcfXMVRCxYFziiwtiyRu1_aem_UOZCbWGwrjXAjVz6jJMVyg
 🔗 Long Context = Real Developer Value
One standout feature being talked about is V4’s ability to handle *very long coding prompts* — far beyond typical context limits. For large software projects, debugging, modular code generation, and architectural reasoning, this is huge: developers don’t have to break problems into small chunks or juggle multiple prompt sessions. 
https://www.techzine.eu/news/analytics/137800/deepseek-to-release-v4-ai-model-with-powerful-coding-capabilities-in-february/?fbclid=IwY2xjawPQG_NleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHoKYsz0SQmDHKh-3LYAFkmHD6c-5PM1dbV39kx-wcfXMVRCxYFziiwtiyRu1_aem_UOZCbWGwrjXAjVz6jJMVyg
🔧 Efficiency Is the Secret Sauce
Facing ongoing export controls and chip restrictions, DeepSeek has doubled down on software and architectural ingenuity instead of brute-force hardware scaling. A recent expansion of its R1 technical paper — released just as the V4 discussion heats up — highlights transparent training pipelines and methods that make big models feasible *without hyperscale compute*. 
https://winbuzzer.com/2026/01/09/deepseek-reveals-r1-model-architecture-secrets-ahead-of-v4-model-launch-xcxwbn/?fbclid=IwY2xjawPQHA1leHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHv2JrfylSJY0HjJrIsKQV3dV622OnfQmvQ9-iiimRYT62aOQhjTHw17h19vB_aem_Lxm-osVxMvn3tpnXLcKptw
 🚩 But the Race Isn’t Just About Raw Performance
DeepSeek’s rise has also attracted regulatory scrutiny and geopolitical tension:
* European regulators recently closed an investigation into hallucination risk after DeepSeek agreed to improve transparency. 
https://www.reuters.com/world/china/italy-closes-probe-into-deepseek-after-commitments-warn-ai-hallucination-risks-2026-01-05/?fbclid=IwY2xjawPQHCxleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHoKYsz0SQmDHKh-3LYAFkmHD6c-5PM1dbV39kx-wcfXMVRCxYFziiwtiyRu1_aem_UOZCbWGwrjXAjVz6jJMVyg
* Privacy and national security concerns have triggered restrictions or bans on DeepSeek in multiple countries, including Australia, Germany, France, and parts of Asia. 
This means any global adoption of V4 will be shaped not only by technology but by data governance and trust issues.
🧩 How This Fits Into the Bigger AI Picture
DeepSeek’s trajectory — from *V3* upgrades to *R1 reasoning breakthroughs* — has already shown how open-source innovation can disrupt expectations:
https://www.forbes.com/sites/tylerroush/2025/03/25/deepseek-launches-ai-model-upgrade-amid-openai-rivalry-heres-what-to-know/?fbclid=IwY2xjawPQHE9leHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHrL2hjrhVEGnnOvGv3B8YyZXoMDGb2nXYrYX6AjH8wWjggPVOdZPREabttkC_aem_0YVZ7uOLUtxI4XwFa0udtQ
* Earlier model releases have *shaken markets* and even triggered stock volatility. 
* DeepSeek’s emphasis on *low training cost and open methodology* has inspired other Chinese AI players and even influenced how Western labs think about open research. 
http://cmp.com/.../deepseek-ends-week-long-marathon... 
Now with V4, DeepSeek isn’t just playing catch-up — it’s targeting a specific vertical where AI tools have immediate economic impact: software engineering and developer productivity. If V4 delivers on its claims, it could shift how enterprises integrate AI into real-world workflows, from code generation to complex system design.
📌 Bottom Line
DeepSeek V4 isn’t just another upgrade — it’s a strategic play:
* Targeted at coding and long-context developer workflows, a growing niche where current models still struggle.
* Built to punch above compute limitations, using smarter training and architecture rather than more chips.
* Emerging from a complex global context where performance is only part of the story — trust, regulation, and geopolitical positioning also matter.
So the question — *“Are you ready to test V4 against your current coding workflow?”* — isn’t just technical. It’s strategic: what it means for code quality, development velocity, and global standards in AI-assisted engineering.
https://www.theinformation.com/articles/deepseek-release-next-flagship-ai-model-strong-coding-ability?fbclid=IwY2xjawPQHIhleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHv2JrfylSJY0HjJrIsKQV3dV622OnfQmvQ9-iiimRYT62aOQhjTHw17h19vB_aem_Lxm-osVxMvn3tpnXLcKptw

Inside NVIDIA GPUs: Anatomy of high performance matmul kernels  (Aleksa Gordić, September 2025)
"In this post, I will gradually introduce all of the core hardware concepts and programming techniques that underpin state-of-the-art (SOTA) NVIDIA GPU matrix-multiplication (matmul) kernels.
Why matmul? Transformers spend most of their FLOPs inside matmuls (linear layers in MLP, attention QKV projections, output projections, etc.) both during training and inference. These operations are embarrassingly parallel, making them a natural fit for GPUs. Finally, understanding how matmul kernels work gives you the toolkit to design nearly any other high-performance GPU kernel.
This post is structured into four parts:
1. Fundamentals of NVIDIA GPU architecture: global memory, shared memory, L1/L2 cache, impact of power throttling on SOL, etc.
2. GPU assembly languages: SASS and PTX
Designing near-SOTA synchronous matmul kernel: the warp-tiling method
3. Designing SOTA asynchronous matmul kernels on Hopper: leveraging tensor cores, TMA, overlapping computation with loads/stores, Hilbert curves, etc.
4. My aim is for this post to be self-contained: detailed enough to stand on its own, yet concise enough to avoid becoming a textbook.
This is the first part of a broader series. In the following posts, I (aspirationally) plan to cover:
- Designing SOTA matmul kernels on Blackwell GPUs
- Exploring GPU architecture through microbenchmarking experiments
- Designing SOTA multi-GPU kernels
- Demistifying memory consistency models (the GPU equivalent of the tokenizer: the critical component that quietly makes the system run, but still puzzles most devs)"
[https://www.aleksagordic.com/blog/matmul](https://www.aleksagordic.com/blog/matmul) 
Diagram:
"At the highest level, a GPU performs two essential tasks:
1. Move and store data (the memory system)
2. Do useful work with the data (the compute pipelines)
The block diagram of H100 below reflects this division: components in blue represent memory or data movement, while components in red are compute (hot) units.

https://pubs.aip.org/aip/pof/article/38/1/015112/3376992/Guiding-diffusion-models-to-reconstruct-flow?fbclid=IwY2xjawPQHUNleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHsM61ULphyLTCtzrtwnixOTPywWos_7TrJ0vlCMXooXsZU-81T0ALX8qghBL_aem_yNvPVUxZPBaqpyMdMjei3Q

https://github.com/songquanpeng/one-api
https://github.com/QuantumNous/new-api
https://github.com/Veloera/Veloera
https://github.com/MartialBE/one-hub
https://github.com/deanxv/done-hub
https://www.api-hub.ai/

https://arxiv.org/abs/2510.26745v1?fbclid=IwY2xjawPQIrhleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHkEiU3u3iY1zfW6qSQ-OtcQRlpSs-rl2nD9czonI1ZzQJW0ymB3150tvUvLc_aem_lEtwvQpP6u76iZL7Gpj6_g
https://arxiv.org/abs/2601.05230v1?fbclid=IwY2xjawPQIs5leHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHoKYsz0SQmDHKh-3LYAFkmHD6c-5PM1dbV39kx-wcfXMVRCxYFziiwtiyRu1_aem_UOZCbWGwrjXAjVz6jJMVyg
https://www.clcoding.com/2025/12/python-with-ai-for-all-2026-complete.html?fbclid=IwY2xjawPQItxleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHkEiU3u3iY1zfW6qSQ-OtcQRlpSs-rl2nD9czonI1ZzQJW0ymB3150tvUvLc_aem_lEtwvQpP6u76iZL7Gpj6_g
https://www.clcoding.com/2025/12/machine-learning-blueprints-with-python.html?fbclid=IwY2xjawPQIvBleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHnxtyNk-Wk9Fc3Z6iYSZULPkb1llTLXW166AH4PRTJ6A71Z6Wb3FbRMY9lfD_aem_Q-lX2ofWuPr2B6Y0lf6Rxg

🎯 Goodbye traditional control... Now AI runs your phone completely with AutoGLM
What Zai announced is not just a new AI model,
A radical change in our relationship with phones and apps 👀📱
AutoGLM launched as a Vision + Language (VLM) model
🔓 100% open source
🤖 And designed to act as an autonomous AI Agent
Artificial Intelligence is no longer enough to answer...
Instead, he sees, understands, and behaves inside your phone just like a human.
---
❇️ What makes AutoGLM a quality carrier?
🔹 Understanding the UI (GUI Understanding)
The model is able to analyze the screen, differentiate icons, lists, buttons, and windows
👈 Then take the right decision and execute the steps with incredible precision, just like the human eye.
🔹 Turning abstract commands into real actions
Your say :
“Book me an appointment”
أوو
"Send a message"
It means, the model will go between the applications, presses, writes, and checks ...
Even complete the task without your extra intervention ⚙️🤯
🔹 Complete independence (Autonomous Action)
Just one order from you...
Then AutoGLM begins planning, executing, and autocorrecting until the goal is reached.
🔹 Sovereign Privacy (Local Execution)
⚠️ The most dangerous and important point
AutoGLM
Working locally (offline)
✔️ don't send data
✔️ No cloud servers
✔️ Do not follow
✔️ No Leaks
Your data ... Remain yours only you 🔐
---
❇️ My personal opinion as a specialist in the field
The core difference here is not just in intelligence...
But in digital control and sovereignty.
Models like: ChatGPT – Gemini – Claude
Very strong no doubt 💪
But it always requires sharing your data with developed companies.
As for the local models like AutoGLM
It restores power to the user
And it's finally giving us what we've long been missing in the age of cloud:
👈 Privacy + Control + True Security
---
🔗 Official sources
📌 GitHub Warehouse (operating steps):
https://github.com/zai-org/Open-AutoGLM
📌 The model on Hugging Face:
https://huggingface.co/zai-org/AutoGLM-Phone-9B-Multilingual
📌 Official Announcement:
https://xiao9905.github.io/AutoGLM/blog.html

https://www.clcoding.com/2025/09/the-complete-machine-learning-engineer.html?fbclid=IwY2xjawPQIxxleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHnxtyNk-Wk9Fc3Z6iYSZULPkb1llTLXW166AH4PRTJ6A71Z6Wb3FbRMY9lfD_aem_Q-lX2ofWuPr2B6Y0lf6Rxg
https://www.clcoding.com/2026/01/machine-learning-essentials-master-core.html?fbclid=IwY2xjawPQIytleHRuA2FlbQIxMABicmlkETBIY3RKREZFTlNoamVIQVp3c3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHsM61ULphyLTCtzrtwnixOTPywWos_7TrJ0vlCMXooXsZU-81T0ALX8qghBL_aem_yNvPVUxZPBaqpyMdMjei3Q
https://www.clcoding.com/2026/01/machine-learning-algorithms-supervised.html
https://www.clcoding.com/2026/01/machine-learning-data-science-ai.html
https://www.clcoding.com/2026/01/python-ai-machine-learning-crash-course.html#google_vignette
https://www.clcoding.com/2026/01/machine-learning-essentials-master-core.html
https://www.clcoding.com/2026/01/applied-machine-learning-with-python.html
https://www.clcoding.com/2026/01/machine-learning-made-simple-clear.html
https://www.clcoding.com/2026/01/the-kaggle-book-master-data-science.html

https://github.com/FlowiseAI/Flowise

Anthropic has launched improved safety classifiers aimed at stopping AI jailbreaks.
The key idea is to add a cheap “early warning” safety check that runs all the time, and only turn on a stronger safety check when something looks suspicious, while also judging the user prompt and the model’s reply together so hidden or coded jailbreak requests do not slip through.
A new “Constitutional Classifiers++” setup stops universal jailbreaks without making the model expensive or annoying to use, by using a cheap internal probe to screen everything and only escalating suspicious chats to a stronger context-aware classifier.
40x less compute than a full exchange classifier, and 0.05% refusals on production traffic.
They proposed an “ensemble cascade” where an exchange classifier reads the prompt and the model’s partial answer together to beat obfuscation tricks, but it runs rarely because a near-free linear probe, built off the model’s own internal activations, decides when escalation is needed.
- The idea
A “Constitutional Classifier” is a separate model whose whole job is to read a conversation and decide whether the assistant should continue or refuse.
“Constitutional” here means the classifier is trained against a written rule set that says what is allowed and what is disallowed, like helping with normal chemistry learning but not with chemical weapon steps.
The core deployment problem is that defenses need to be cheap and rarely block normal users, because even a tiny refusal rate becomes real friction at scale.
This paper treats compute cost and refusal rate as first-class constraints, not afterthoughts, and the whole design is built around that.
- What broke in the last system
The earlier setup split the job into 2 separate checks, one model looked only at the user input, and another looked only at the assistant output.
That split sounds clean, but it creates a blind spot when the harmful meaning is distributed across the prompt and the reply, so neither side looks bad alone.
Reconstruction-style attacks exploit this by hiding a harmful request inside a larger harmless-looking blob, then asking the model to piece it back together while answering.
Obfuscation-style attacks exploit it by pushing the model to speak in code words, riddles, or substitutions that look safe if the output is judged without the prompt context.
Some of these attack styles also damage normal model capability, and the paper shows GPQA Diamond accuracy dropping from 74.2% to 32.3% under 1 such jailbreak pattern, which signals the attack is “expensive” but still not something to rely on.
- The image is showing 2 common ways jailbreakers beat the older “Constitutional Classifiers” setup by hiding the real request across context.
On the left, the attacker splits a harmful request into harmless-looking pieces inside code, then tells the model to reconstruct it, so the input filter misses the intent.
On the right, the attacker uses metaphors and indirect language so the output filter thinks the reply is harmless, even though it becomes harmful once you read it together with the prompt.
The big message is that checking the user prompt and the model output separately creates a blind spot, so the paper’s proposal is to judge them together in context to catch these tricks.
- The 2-stage cascade that saves compute
The cascade idea is simple: run a cheap first check on everything, and run the expensive check only on the small fraction that looks suspicious.
The key product choice is that stage 1 does not refuse the user, it escalates to stage 2, so stage 1 can be “trigger-happy” without annoying users too much.
This is basically adaptive compute for safety, where boring normal chats get the cheap path and only weird chats pay the expensive path.
With updated models and pipeline tweaks, the 2-stage system cut the exchange-classifier overhead by a factor of 5.4, with about 10% of traffic routed to the expensive second stage in their calibration.
A false positive in stage 1 mostly means “pay more compute,” while a false positive in the final stage means “a user got refused,” so this separation matters a lot in production.
- Why probe plus classifier beats either alone
A probe can be strong and still miss stuff, and a fine-tuned external classifier can be strong and still miss different stuff, so the paper leans on ensembling.
They show the probe and the external classifier disagree more often than 2 external classifiers disagree, which is exactly what is wanted from an ensemble because it means fewer shared blind spots.
The paper measures that “disagree more often” idea with Spearman rank correlation, and the probe paired with the small classifier has lower correlation than the small paired with the extra-small classifier.
They also use the probe as a router, where low-confidence moments trigger the external classifier, and then the final decision mixes both scores.
On their dataset, that routing approach can beat the small classifier’s robustness while cutting external-classifier compute by about 100x, because the expensive model is skipped most of the time.
anthropic.com/research/next-generation-constitutional-classifiers

ghttps://ithub.com/k4yt3x/video2x

https://github.com/Agenta-AI/agenta

GDPO: Group reward-Decoupled Normalization Policy Optimization for Multi-reward RL Optimization (NVIDIA, January 2026) 
Paper: [https://arxiv.org/abs/2601.05242](https://arxiv.org/abs/2601.05242) 
Abstract:
"As language models become increasingly capable, users expect them to provide not only accurate responses but also behaviors aligned with diverse human preferences across a variety of scenarios. To achieve this, Reinforcement learning (RL) pipelines have begun incorporating multiple rewards, each capturing a distinct preference, to guide models toward these desired behaviors. However, recent work has defaulted to apply Group Relative Policy Optimization (GRPO) under multi-reward setting without examining its suitability. In this paper, we demonstrate that directly applying GRPO to normalize distinct rollout reward combinations causes them to collapse into identical advantage values, reducing the resolution of the training signal and resulting in suboptimal convergence and, in some cases, early training failure. We then introduce Group reward-Decoupled Normalization Policy Optimization (GDPO), a new policy optimization method to resolve these issues by decoupling the normalization of individual rewards, more faithfully preserving their relative differences and enabling more accurate multi-reward optimization, along with substantially improved training stability. We compare GDPO with GRPO across three tasks: tool calling, math reasoning, and coding reasoning, evaluating both correctness metrics (accuracy, bug ratio) and constraint adherence metrics (format, length). Across all settings, GDPO consistently outperforms GRPO, demonstrating its effectiveness and generalizability for multi-reward reinforcement learning optimization."

Open-sourced Falcon H1R 7B delivers state-of-the-art reasoning while using just 7B parameters - matching or beating models up to 7× larger.
A great start to 2026: A 7b model with 88% in AIME 24 and 83% in AIME 25.
link https://falconllm.tii.ae/falcon-h1r-7b.html

n8n to code 
https://docs.n8n.io/code/

toolkit for compressing, deploying, and serving LLMs. 
https://github.com/InternLM/lmdeploy

Learning Latent Action World Models In The Wild 
Quentin Garrido, Tushar Nagarajan, Basile Terver, Nicolas Ballas, Yann LeCun, Michael Rabbat 
FAIR at Meta, INRIA, New York University 2026 
https://arxiv.org/abs/2601.05230 
For an AI system to plan and act intelligently in the real world, it needs a way to imagine the future: *if I do this, what will happen next?* Researchers often tackle this using world models—systems that learn how the world evolves in response to actions. The catch is that most of these models rely on clearly labeled actions (“move left,” “pick up object”), which are expensive and sometimes impossible to collect at scale.
This work explores a more ambitious idea: learning what actions are directly from videos, without any labels at all. Instead of being told what an action is, the model infers a hidden—or *latent*—action space by watching how scenes change over time. What makes this study stand out is that it moves beyond tidy environments like video games or robot simulators and tackles “in-the-wild” videos—the messy, diverse footage of real life.
That realism comes with challenges. Videos differ wildly in lighting, camera angles, backgrounds, and even in what kind of “agent” is acting—sometimes it’s a person, sometimes an animal, sometimes no obvious actor at all. There is also no shared body or viewpoint across videos, unlike in robotics where a single robot is always present.
The authors show that these challenges can be addressed by carefully designing how latent actions are represented. They find that continuous but constrained action representations work far better than popular discrete approaches. With this setup, the model can capture surprisingly rich behaviors. For example, it can learn that “a person entering a room” is a meaningful action-like change—and recognize or transfer that concept across completely different videos.
Because there is no single physical body shared across videos, the learned actions tend to be spatially localized—tied to regions in the camera’s view rather than to a specific agent’s limbs. Even so, the researchers demonstrate something powerful: they can train a controller that maps familiar, human-defined actions onto these learned latent actions. This effectively turns the latent action space into a **universal interface** for planning.
When used for decision-making and planning, the resulting system performs on par with traditional models that rely on explicit action labels. Overall, this work marks an important step toward AI systems that can learn how actions work directly from real-world video, bringing world models closer to functioning outside controlled lab settings and into the complexity of everyday life. 
Recent trends often emphasize:
*Scale
*Bigger transformers
*Longer rollouts
This paper emphasizes:
*What should count as an action
*What structure actions must obey
*How actions arise from observation, not annotation
In that sense, it’s less incremental and more foundational. 
While most world-model studies assume actions and scale prediction, this work asks how actions themselves can be discovered from real-world video—and shows that doing so changes both the architecture and the nature of planning. 
Dreamer and MuZero assume actions; Genie inherits them from games; V-JEPA ignores them—this work discovers them, in the wild, and makes them usable for planning. 
This paper weakens the necessity of embodiment for acquiring agency, while strengthening the case that embodiment is a grounding layer rather than the source of intelligence itself.

Reordering the same RAG documents can flip an LLM's answer, Stable-RAG makes it stay consistent.
Stable-RAG stops RAG answers from changing when the retrieved evidence is shown in a different order.
Even when the correct passage is present, sometimes even first, the model's internal reasoning can drift, and a harmless reorder can trigger a hallucination, meaning a made-up fact.
Stable-RAG deals with this by running the LLM on many different document orders, grabbing its final hidden state, meaning its last internal summary, and grouping those summaries to find the dominant reasoning path.
It then decodes answers from the center of each group and uses Direct Preference Optimization, a training method that prefers better answers over worse ones, to push the model toward consistent, evidence-grounded outputs or "I don't know".
On 3 question answering datasets with 2 retrievers, meaning 2 ways to fetch documents, Stable-RAG improves accuracy and keeps answers stable across reorders, so a small shuffle does not change what the system says.
– https://arxiv.org/abs/2601.02993

SPIRAL: Symbolic LLM Planning via Grounded and Reflective Search (IBM T.J. Watson Research Center, December 2025)
Paper: [https://arxiv.org/abs/2512.23167](https://arxiv.org/abs/2512.23167) 
Abstract:
"Large Language Models (LLMs) often falter at complex planning tasks that require exploration and self-correction, as their linear reasoning process struggles to recover from early mistakes. While search algorithms like Monte Carlo Tree Search (MCTS) can explore alternatives, they are often ineffective when guided by sparse rewards and fail to leverage the rich semantic capabilities of LLMs. We introduce SPIRAL (Symbolic LLM Planning via Grounded and Reflective Search), a novel framework that embeds a cognitive architecture of three specialized LLM agents into an MCTS loop. SPIRAL's key contribution is its integrated planning pipeline where a Planner proposes creative next steps, a Simulator grounds the search by predicting realistic outcomes, and a Critic provides dense reward signals through reflection. This synergy transforms MCTS from a brute-force search into a guided, self-correcting reasoning process. On the DailyLifeAPIs and HuggingFace datasets, SPIRAL consistently outperforms the default Chain-of-Thought planning method and other state-of-the-art agents. More importantly, it substantially surpasses other state-of-the-art agents; for example, SPIRAL achieves 83.6% overall accuracy on DailyLifeAPIs, an improvement of over 16 percentage points against the next-best search framework, while also demonstrating superior token efficiency. Our work demonstrates that structuring LLM reasoning as a guided, reflective, and grounded search process yields more robust and efficient autonomous planners. The source code, full appendices, and all experimental data are available for reproducibility at the official project repository."

SPICE so an LLM can learn good actions from small context, even with bad training logs.
The problem is that in context reinforcement learning, meaning learning from a short log without changing weights, often gets stuck copying the old policy.
SPICE learns a value prior, meaning a starting guess for how good each action is, and it learns how unsure that guess is.
On a new task, it treats the recent log as new evidence, focuses on past moments similar to the current state, and updates each action score.
The authors test it in bandits, meaning repeated choices among options with unknown rewards, and in a simple navigation control task, using weak training data.
They report that SPICE adapts quickly on unseen tasks and keeps regret, meaning lost reward versus the best possible, lower than earlier baselines.
It matters because it explores by adding an uncertainty bonus to each action score, and a bad starting guess only hurts early.
https://arxiv.org/abs/2601.03015

Introducing Digital Red Queen (DRQ): Adversarial Program Evolution in Core War with LLMs
Blog: https://sakana.ai/drq
Core War is a programming game where self-replicating assembly programs, called warriors, compete for control of a virtual machine. In this dynamic environment, where there is no distinction between code and data, warriors must crash opponents while defending themselves to survive.
In this work, we explore how LLMs can drive open-ended adversarial evolution of these programs within Core War. Our approach is inspired by the Red Queen Hypothesis from evolutionary biology: the principle that species must continually adapt and evolve simply to survive against ever-changing competitors.
We found that running our DRQ algorithm for longer durations produces warriors that become more generally robust. Most notably, we observed an emergent pressure towards convergent evolution. Independent runs, starting from completely different initial conditions, evolved toward similar general-purpose behaviors—mirroring how distinct species in nature often evolve similar traits to solve the same problems.
Simulating these adversarial dynamics in an isolated sandbox offers a glimpse into the future, where deployed LLM systems might eventually compete against one another for computational or physical resources in the real world.
This project is a collaboration between MIT and Sakana AI led by 
@akarshkumar0101
Full Paper (Website): https://pub.sakana.ai/drq/
Full Paper (arxiv): https://arxiv.org/abs/2601.03335
Code: https://github.com/SakanaAI/drq/

## 🛠️ Self-Improvement Protocol
To stabilize the fleet after research implementation, run the following command:
```powershell
C:/DEV/PyAgent/.venv/Scripts/python.exe src/infrastructure/dev/scripts/run_fleet_self_improvement.py -c 50 -p docs\notes\note.txt
```
This performs 50 autonomous cycles of code quality, security, and technical debt optimization while following the strategic directive in `note.txt`.

recusrsively visit all of these: https://arxiv.org/list/cs.AI/recent?skip=0&show=2000
