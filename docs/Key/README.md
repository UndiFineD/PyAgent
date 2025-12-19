# Key AI Concepts & Architecture Documentation

This directory contains detailed explanations of advanced Artificial Intelligence concepts, architectures, and optimization techniques. Below is a guide to the documents in this section, organized by category.

## 1. Introduction & History
*   **[History of AI](History-of-AI.md)**: (Implicitly covered in sections below)
*   **[Turing-Test.md](Turing-Test.md)**: The Imitation Game proposed by Alan Turing (1950) to test machine intelligence.
*   **[AI-Winters.md](AI-Winters.md)**: Periods of reduced funding and interest (1974-1980, 1987-1993) caused by overpromising and underdelivering.
*   **[Expert-Systems.md](Expert-Systems.md)**: Rule-based systems (MYCIN, DENDRAL) that dominated AI in the 1980s.
*   **[Deep-Learning-Revolution.md](Deep-Learning-Revolution.md)**: The resurgence of Neural Networks starting with AlexNet (2012) and the availability of GPUs.

## 2. Mathematics & Fundamentals
*   **[Linear-Algebra.md](Linear-Algebra.md)**: The language of AI. Vectors, Matrices, Tensors, Dot Products, and Eigenvalues.
*   **[Calculus-for-ML.md](Calculus-for-ML.md)**: The engine of learning. Derivatives, Gradients, Chain Rule, and Jacobians.
*   **[Probability-Theory.md](Probability-Theory.md)**: Quantifying uncertainty. Bayes' Theorem, Distributions (Gaussian, Bernoulli), and Maximum Likelihood Estimation.
*   **[Information-Theory.md](Information-Theory.md)**: Measuring information. Entropy, Cross-Entropy, KL Divergence, and Mutual Information.
*   **[Graph-Theory-Fundamentals.md](Graph-Theory-Fundamentals.md)**: The study of graphs (nodes and edges), essential for GNNs and Knowledge Graphs.
*   **[Game-Theory-Fundamentals.md](Game-Theory-Fundamentals.md)**: Mathematical models of strategic interaction (Nash Equilibrium, Minimax) used in GANs and Multi-Agent Systems.

## 3. Deep Learning Theory
*   **[Universal-Approximation-Theorem.md](Universal-Approximation-Theorem.md)**: The mathematical proof that Neural Networks can approximate any continuous function.
*   **[No-Free-Lunch-Theorem.md](No-Free-Lunch-Theorem.md)**: The principle that no single algorithm works best for every possible problem.
*   **[Bias-Variance-Tradeoff.md](Bias-Variance-Tradeoff.md)**: The fundamental conflict between minimizing bias (underfitting) and variance (overfitting).
*   **[Double-Descent.md](Double-Descent.md)**: The phenomenon where test error decreases, increases, and then decreases again as model size grows.
*   **[Lottery-Ticket-Hypothesis.md](Lottery-Ticket-Hypothesis.md)**: The theory that dense networks contain sparse subnetworks that can be trained to the same accuracy.
*   **[Grokking.md](Grokking.md)**: A phase transition where a model suddenly generalizes long after it has memorized the training data.
*   **[Neural-Tangent-Kernel.md](Neural-Tangent-Kernel.md)**: **NTK**. Analyzing the training dynamics of infinite-width neural networks.
*   **[Curse-of-Dimensionality.md](Curse-of-Dimensionality.md)**: Why data becomes sparse and distance metrics lose meaning in high-dimensional spaces.

## 4. Foundational Neural Networks
*   **[Perceptrons-and-MLPs.md](Perceptrons-and-MLPs.md)**: The fundamental building blocks of Deep Learning. Activation functions and Backpropagation.
*   **[Kolmogorov-Arnold-Networks.md](Kolmogorov-Arnold-Networks.md)**: **KANs**. A novel alternative to MLPs with learnable activation functions on edges (splines) instead of fixed weights on nodes.
*   **[Convolutional-Neural-Networks.md](Convolutional-Neural-Networks.md)**: **CNNs**. The architecture that revolutionized Computer Vision (Kernels, Pooling, ResNet).
*   **[Recurrent-Neural-Networks.md](Recurrent-Neural-Networks.md)**: **RNNs**. Processing sequential data with internal memory (LSTMs, GRUs).
*   **[Autoencoders.md](Autoencoders.md)**: Unsupervised learning for data compression and reconstruction (VAEs).

## 5. Training & Optimization
*   **[Optimization-Algorithms.md](Optimization-Algorithms.md)**: How models learn. SGD, Adam, AdamW, and Schedule-Free optimization.
*   **[Gradient-Descent-Variants.md](Gradient-Descent-Variants.md)**: Beyond SGD. Momentum, RMSProp, and Adagrad.
*   **[Learning-Rate-Schedulers.md](Learning-Rate-Schedulers.md)**: Techniques to adjust the learning rate during training. Cosine Annealing, Warmup.
*   **[Loss-Functions.md](Loss-Functions.md)**: The mathematical objective the model tries to minimize. MSE, Cross-Entropy, Focal Loss, and Triplet Loss.
*   **[Regularization-Techniques.md](Regularization-Techniques.md)**: Preventing overfitting. L1/L2 Regularization, Dropout, and Weight Decay.
*   **[Initialization-Methods.md](Initialization-Methods.md)**: Setting starting weights correctly. Xavier (Glorot) and He (Kaiming) initialization.
*   **[Normalization-Methods.md](Normalization-Methods.md)**: Techniques to stabilize training. Batch Norm, Layer Norm, and RMSNorm.
*   **[Batch-Size-Effects.md](Batch-Size-Effects.md)**: How batch size impacts generalization gap and training speed.
*   **[Gradient-Clipping.md](Gradient-Clipping.md)**: Preventing exploding gradients by capping the norm of the gradient vector.
*   **[Label-Smoothing.md](Label-Smoothing.md)**: A regularization technique that prevents the model from becoming too confident in its predictions.
*   **[Mixed-Precision-Training.md](Mixed-Precision-Training.md)**: Using lower precision (FP16/BF16) to speed up training and reduce memory usage.
*   **[Hyperparameter-Optimization.md](Hyperparameter-Optimization.md)**: Finding the best configuration for a model. Grid Search, Random Search, and Bayesian Optimization (Optuna).
*   **[Model-Merging.md](Model-Merging.md)**: Combining weights of multiple trained models. Model Soups, SLERP, and DARE.
*   **[Activations-Pre.md](Activations-Pre.md)** & **[Activations-Post.md](Activations-Post.md)**: Analysis of neural states before and after activation functions.

## 6. Core Architectures
*   **[Attention.md](Attention.md)**: Explains the "Attention Is All You Need" paper, the Self-Attention mechanism (Query, Key, Value).
*   **[Ring-Attention.md](Ring-Attention.md)**: Technique for processing infinite context windows by distributing the attention calculation across devices in a ring.
*   **[Linear-Attention-RWKV.md](Linear-Attention-RWKV.md)**: **RWKV**. Architectures that achieve Transformer-level performance with RNN-level (linear) inference cost.
*   **[Transformers.md](Transformers.md)**: Covers the broader Transformer family (Encoder-only, Decoder-only, Encoder-Decoder).
*   **[Diffusion-Models.md](Diffusion-Models.md)**: Details Diffusion Models (Forward/Reverse process, U-Nets) used for image generation.
*   **[Diffusion-Transformers.md](Diffusion-Transformers.md)**: **DiT**. Replacing the U-Net backbone with Transformers for scalable video/image generation (Sora, SD3).
*   **[Flow-Matching.md](Flow-Matching.md)**: A generalization of diffusion based on Optimal Transport, allowing for straighter generation paths and faster inference.
*   **[Consistency-Trajectory-Models.md](Consistency-Trajectory-Models.md)**: **CTM**. Single-step generative models that distill the diffusion process.
*   **[Generative-Adversarial-Networks.md](Generative-Adversarial-Networks.md)**: **GANs**. The adversarial architecture (Generator vs. Discriminator).
*   **[Mixture-of-Experts.md](Mixture-of-Experts.md)**: **MoE**. Architectures that use multiple specialized sub-networks (experts).
*   **[Mixture-of-Depths.md](Mixture-of-Depths.md)**: **MoD**. Dynamically allocating compute (layers) per token, allowing some tokens to skip processing steps.
*   **[State-Space-Models.md](State-Space-Models.md)**: **SSMs**. Alternatives to Transformers (like Mamba) that offer linear scaling.
*   **[Memory-Augmented-Neural-Networks.md](Memory-Augmented-Neural-Networks.md)**: **MANNs**. Neural Turing Machines (NTM) and Differentiable Neural Computers (DNC) that decouple memory from computation.
*   **[Liquid-Neural-Networks.md](Liquid-Neural-Networks.md)**: **LNNs**. Time-continuous RNNs that adapt to changing data distributions.
*   **[Graph-Neural-Networks.md](Graph-Neural-Networks.md)**: **GNNs**. Models designed to process graph-structured data.
*   **[Neural-Architecture-Search.md](Neural-Architecture-Search.md)**: **NAS**. Automating the design of neural networks using AI.
*   **[Continuous-Thought-Machine.md](Continuous-Thought-Machine.md)**: **Continuous Chain of Thought**. Reasoning in latent space.

## 7. Famous Architectures
*   **[Capsule-Networks.md](Capsule-Networks.md)**: **CapsNets**. Hinton's architecture designed to handle spatial hierarchies and pose relationships better than CNNs.
*   **[ResNet.md](ResNet.md)**: **Residual Networks**. Solved the vanishing gradient problem using skip connections.
*   **[U-Net.md](U-Net.md)**: The U-shaped architecture with skip connections, backbone of Diffusion models.
*   **[BERT.md](BERT.md)**: **Bidirectional Encoder Representations from Transformers**. Masked Language Modeling.
*   **[GPT-Series.md](GPT-Series.md)**: **Generative Pre-trained Transformer**. Evolution from GPT-1 to GPT-4.
*   **[Llama.md](Llama.md)**: Meta's open-weights LLM that democratized access to powerful language models.
*   **[Vision-Transformers.md](Vision-Transformers.md)**: **ViT**. Applying Transformers to image patches.
*   **[CLIP.md](CLIP.md)**: **Contrastive Language-Image Pre-training**. Connecting text and images.
*   **[Stable-Diffusion.md](Stable-Diffusion.md)**: Latent Diffusion Model (LDM) for text-to-image generation.
*   **[ControlNet.md](ControlNet.md)**: Controlling diffusion models with extra conditions (edges, depth, pose).
*   **[Whisper.md](Whisper.md)**: OpenAI's robust multilingual speech recognition model.
*   **[YOLO.md](YOLO.md)**: **You Only Look Once**. Real-time object detection.
*   **[AlphaGo.md](AlphaGo.md)**: Deep RL system that defeated the world champion at Go.

## 8. Applied AI Domains

### Computer Vision
*   **[Computer-Vision.md](Computer-Vision.md)**: Core visual tasks beyond generation.
*   **[Object-Detection-Models.md](Object-Detection-Models.md)**: Identifying and locating objects. R-CNN, SSD, RetinaNet.
*   **[Image-Segmentation-Types.md](Image-Segmentation-Types.md)**: Semantic, Instance, and Panoptic Segmentation.
*   **[Face-Recognition.md](Face-Recognition.md)**: Siamese Networks, Triplet Loss, and ArcFace.
*   **[Optical-Character-Recognition.md](Optical-Character-Recognition.md)**: **OCR**. Tesseract, CRNN, and TrOCR.
*   **[Pose-Estimation.md](Pose-Estimation.md)**: Detecting human keypoints. OpenPose and MediaPipe.
*   **[3D-Reconstruction.md](3D-Reconstruction.md)**: Photogrammetry, SfM, NeRFs, and Gaussian Splatting.
*   **[Video-Object-Tracking.md](Video-Object-Tracking.md)**: SORT, DeepSORT, and Kalman Filters.
*   **[Image-Restoration.md](Image-Restoration.md)**: Super-Resolution, Denoising, and Inpainting.
*   **[Video-Generation.md](Video-Generation.md)**: Spacetime Patches, DiT, and Sora.
*   **[Video-Understanding.md](Video-Understanding.md)**: Action Recognition, Temporal Modeling (TimeSformer, VideoMAE).
*   **[3D-Generation.md](3D-Generation.md)**: Creating 3D assets from text/images.

### Natural Language Processing (NLP)
*   **[Natural-Language-Understanding.md](Natural-Language-Understanding.md)**: **NLU**. NER, Sentiment Analysis, POS Tagging.
*   **[Machine-Translation.md](Machine-Translation.md)**: **NMT**. Seq2Seq, Attention, BLEU.
*   **[Text-Summarization.md](Text-Summarization.md)**: Extractive vs. Abstractive methods.
*   **[Tokenization.md](Tokenization.md)**: BPE, WordPiece, SentencePiece.

### Audio & Speech
*   **[Speech-Recognition.md](Speech-Recognition.md)**: **ASR**. CTC, RNN-T.
*   **[Audio-Generation.md](Audio-Generation.md)**: TTS and Music Generation (MusicGen, AudioLDM).

### Reinforcement Learning (RL)
*   **[Reinforcement-Learning.md](Reinforcement-Learning.md)**: **RL**. Agents, Environments, Rewards.
*   **[Q-Learning.md](Q-Learning.md)**: Value-based methods, Bellman Equation.
*   **[Deep-Q-Networks.md](Deep-Q-Networks.md)**: **DQN**. Deep RL for complex environments.
*   **[Policy-Gradients.md](Policy-Gradients.md)**: REINFORCE and direct policy optimization.
*   **[Proximal-Policy-Optimization.md](Proximal-Policy-Optimization.md)**: **PPO**. The industry standard for RL and RLHF.
*   **[Multi-Agent-RL.md](Multi-Agent-RL.md)**: **MARL**. Cooperative and Competitive agents.
*   **[World-Models.md](World-Models.md)**: Model-Based RL and internal simulations.
*   **[Decision-Transformers.md](Decision-Transformers.md)**: Treating Reinforcement Learning as a sequence modeling problem.

### Other Domains
*   **[Recommender-Systems.md](Recommender-Systems.md)**: Collaborative Filtering, DLRM.
*   **[Recommendation-Architectures.md](Recommendation-Architectures.md)**: Modern architectures. Two-Tower Models, DLRM, and Session-based RNNs.
*   **[Time-Series-Forecasting.md](Time-Series-Forecasting.md)**: ARIMA, Temporal Fusion Transformers.
*   **[Time-Series-Foundation-Models.md](Time-Series-Foundation-Models.md)**: Zero-shot forecasting with Chronos, Lag-Llama, and Moirai.
*   **[Anomaly-Detection.md](Anomaly-Detection.md)**: Autoencoders, Isolation Forests.
*   **[AI-for-Science.md](AI-for-Science.md)**: AlphaFold, Material Discovery, PINNs.
*   **[Embodied-AI.md](Embodied-AI.md)**: **Robotics**. Sim2Real transfer.
*   **[Visual-Language-Action-Models.md](Visual-Language-Action-Models.md)**: **VLA**. Models that output robot actions directly from vision/text (RT-2, PaLM-E).
*   **[AI-in-Healthcare.md](AI-in-Healthcare.md)**: Medical Imaging, Drug Discovery, Clinical Support.
*   **[AI-in-Finance.md](AI-in-Finance.md)**: Algorithmic Trading, Fraud Detection, Risk Management.
*   **[AI-in-Education.md](AI-in-Education.md)**: Intelligent Tutoring Systems, Personalized Learning.
*   **[AI-in-Cybersecurity.md](AI-in-Cybersecurity.md)**: Threat Detection, Phishing Analysis, SOC Automation.

## 9. Generative AI & Foundation Models
*   **[Foundation-Models.md](Foundation-Models.md)**: Large-scale models adaptable to downstream tasks.
*   **[Multimodal-Models.md](Multimodal-Models.md)**: Processing Text+Image, Audio (CLIP, LLaVA).
*   **[Retrieval-Augmented-Generation.md](Retrieval-Augmented-Generation.md)**: **RAG**. Grounding LLMs with external data.
*   **[Vector-Databases.md](Vector-Databases.md)**: Storage for RAG (HNSW, Faiss).
*   **[Vector-Search-Algorithms.md](Vector-Search-Algorithms.md)**: The internals of vector indexing. HNSW, IVF, Product Quantization (PQ), and DiskANN.
*   **[Hybrid-Search.md](Hybrid-Search.md)**: Combining Dense (Vector) and Sparse (Keyword) search for better retrieval (Reciprocal Rank Fusion).
*   **[Embedding-Models.md](Embedding-Models.md)**: Word2Vec, GloVe, Sentence-BERT.
*   **[Prompt-Engineering.md](Prompt-Engineering.md)**: Zero-shot, CoT, System Prompts.
*   **[Adtrieval-Enhanced-Transformer.md](Retrieval-Enhanced-Transformer.md)**: **RETRO**. Architecture that retrieves information from a massive database *during* the generation process (chunked cross-attention).
*   **[Revanced-RAG-Patterns.md](Advanced-RAG-Patterns.md)**: HyDE, Sentence Window Retrieval, and Parent Document Retrieval.
*   **[Reranking-Models.md](Reranking-Models.md)**: Improving retrieval precision with Cross-Encoders (Cohere).
*   **[GraphRAG.md](GraphRAG.md)**: Using Knowledge Graphs to structure and retrieve information for LLMs.
*   **[Sampling-Strategies.md](Sampling-Strategies.md)**: Controlling randomness. Temperature, Top-k, Top-p (Nucleus), and Min-p.
*   **[Beam-Search.md](Beam-Search.md)**: Exploring multiple potential outputs to find the most likely sequence.
*   **[Speculative-Decoding.md](Speculative-Decoding.md)**: Accelerating inference by using a small draft model to predict tokens.
*   **[Guided-Generation.md](Guided-Generation.md)**: Constraining model output to specific formats (JSON, Regex, Grammars).
*   **[Synthetic-Data-Generation.md](Synthetic-Data-Generation.md)**: Self-instruct, evol-instruct.

## 10. Systems, Infrastructure & MLOps
*   **[MLOps.md](MLOps.md)**: Lifecycle of ML engineering.
*   **[Distributed-Training.md](Distributed-Training.md)**: DDP, FSDP, Tensor/Pipeline Parallelism.
*   **[Distributed-Synchronization.md](Distributed-Synchronization.md)**: NCCL, Barriers.
*   **[Federated-Learning.md](Federated-Learning.md)**: Privacy-preserving decentralized training.
*   **[Split-Learning.md](Split-Learning.md)**: Training models by splitting layers across client and server to protect data.
*   **[Model-Compression.md](Model-Compression.md)**: Pruning and Quantization.
*   **[Quantization-Formats.md](Quantization-Formats.md)**: Specific formats for efficient inference. GGUF, AWQ, GPTQ, and EXL2.
*   **[Local-Inference.md](Local-Inference.md)**: Llama.cpp, Ollama, GGUF.
*   **[Edge-AI.md](Edge-AI.md)**: **TinyML**. TFLite, ONNX Runtime.
*   **[Model-Serving.md](Model-Serving.md)**: vLLM, TGI, Triton.
*   **[Model-Routing.md](Model-Routing.md)**: Architectures for dynamically routing queries to the best model (LLM Cascades).
*   **[Feature-Stores.md](Feature-Stores.md)**: Feast, Tecton.
*   **[Data-Lakehouses.md](Data-Lakehouses.md)**: Delta Lake, Iceberg.
*   **[Workflow-Orchestration.md](Workflow-Orchestration.md)**: Airflow, Dagster.
*   **[Experiment-Tracking.md](Experiment-Tracking.md)**: MLflow, Weights & Biases.
*   **[Observability-for-LLMs.md](Observability-for-LLMs.md)**: Tracing, Spans, and monitoring cost/latency (LangSmith, Arize).
*   **[Data-Version-Control.md](Data-Version-Control.md)**: **DVC**.
*   **[Kubernetes-for-AI.md](Kubernetes-for-AI.md)**: Kubeflow, KServe, Ray.
*   **[AI-Accelerators.md](AI-Accelerators.md)**: GPUs, TPUs, LPUs.
*   **[GPU-Programming.md](GPU-Programming.md)**: Low-level programming for AI hardware. CUDA, Kernels, and Triton.
*   **[Cloud-AI-Platforms.md](Cloud-AI-Platforms.md)**: Managed services for AI. AWS SageMaker, Google Vertex AI, Azure AI.
*   **[HuggingFace-Ecosystem.md](HuggingFace-Ecosystem.md)**: Transformers, Datasets, Hub.
*   **[GraphQL.md](GraphQL.md)**: Efficient data retrieval for agents.

## 11. AI in Software Engineering
*   **[Code-LLMs.md](Code-LLMs.md)**: FIM, Repository-level context.
*   **[Fine-Tuning-Code-LLMs.md](Fine-Tuning-Code-LLMs.md)**: Training on internal codebases.
*   **[AI-for-Code-Review.md](AI-for-Code-Review.md)**: Automated PR analysis.
*   **[AI-in-DevSecOps.md](AI-in-DevSecOps.md)**: Vulnerability detection.
*   **[Git-Automation-Agents.md](Git-Automation-Agents.md)**: Commit messages, PR descriptions.
*   **[Automated-Test-Generation.md](Automated-Test-Generation.md)**: PyTest, JUnit generation.
*   **[RAG-for-Codebases.md](RAG-for-Codebases.md)**: AST parsing, GraphRAG.
*   **[Semantic-Code-Search.md](Semantic-Code-Search.md)**: Embedding-based code search.
*   **[AI-Driven-Refactoring.md](AI-Driven-Refactoring.md)**: Modernizing legacy code.
*   **[AI-Fuzzing.md](AI-Fuzzing.md)**: Generative security testing.
*   **[Self-Healing-Systems.md](Self-Healing-Systems.md)**: Auto-remediation.
*   **[Infrastructure-as-Code-AI.md](Infrastructure-as-Code-AI.md)**: Terraform, Ansible generation.
*   **[AIOps.md](AIOps.md)**: IT Operations automation.
*   **[Text-to-SQL.md](Text-to-SQL.md)**: Database interaction.
*   **[Documentation-Automation.md](Documentation-Automation.md)**: Generating docstrings/READMEs.
Geometric-Deep-Learning.md](Geometric-Deep-Learning.md)**: Generalizing neural networks to non-Euclidean domains (Graphs, Manifolds) using symmetry and invariance.
*   **[Energy-Based-Models.md](Energy-Based-Models.md)**: **EBMs**. Learning an energy function to model data distributions (LeCun).
*   **[Active-Inference.md](Active-Inference.md)**: The Free Energy Principle and predictive coding as a unified theory of brain and AI.
*   **[Contrastive-Learning.md](Contrastive-Learning.md)**: SimCLR, CLIP.
*   **[Self-Supervised-Learning.md](Self-Supervised-Learning.md)**: Masked Autoencoders.
*   **[Mechanistic-Interpretability.md](Mechanistic-Interpretability.md)**: Monosemanticity, Circuits.
*   **[Sparse-Autoencoders.md](Sparse-Autoencoders.md)**: **SAEs**. Unsupervised method to decompose model activations into interpretable features.
*   **[Explainable-AI.md](Explainable-AI.md)**: **XAI**. SHAP, LIME.
*   **[Causal-AI.md](Causal-AI.md)**: Pearl's Ladder of Causation.
*   **[Meta-Learning.md](Meta-Learning.md)**: Learning to Learn (MAML).
*   **[Continual-Learning.md](Continual-Learning.md)**: Techniques to prevent Catastrophic Forgetting in lifelong learning agents.
*   **[Generative-Flow-Networks.md](Generative-Flow-Networks.md)**: **GFlowNets**. Probabilistic framework for generating compositional objects with probability proportional to a reward (Bengio).
*   **[Neural-ODEs.md](Neural-ODEs.md)**: Modeling deep networks as continuous-time differential equations.
*   **[Implicit-Neural-Representations.md](Implicit-Neural-Representations.md)**: **INRs**. Representing signals (images, 3D scenes) as continuous functions (SIRENs, NeRFs) rather than discrete grids.
*   **[Synaptic-Plasticity.md](Synaptic-Plasticity.md)**: Biological inspiration.
*   **[Neuromorphic-Computing.md](Neuromorphic-Computing.md)**: Spiking Neural Networks.
*   **[Quantum-Machine-Learning.md](Quantum-Machine-Learning.md)**: **QML**.
*   **[Neuro-Symbolic-AI.md](Neuro-Symbolic-AI.md)**: Combining the learning capability of Neural Networks with the reasoning power of Symbolic Logic (Logic Tensor Networks).
*   **[Hyperdimensional-Computing.md](Hyperdimensional-Computing.md)**: **HDC**. Computing with massive, holographic random vectors (Vector Symbolic Architectures).
*   **[Bayesian-Machine-Learning.md](Bayesian-Machine-Learning.md)**: Probabilistic ML.
*   **[Evolutionary-Algorithms.md](Evolutionary-Algorithms.md)**: Genetic Algorithms.
*   **[Swarm-Intelligence.md](Swarm-Intelligence.md)**: PSO.
*   **[Symbolic-AI.md](Symbolic-AI.md)**: Neuro-Symbolic AI.
*   **[Ensemble-Learning.md](Ensemble-Learning.md)**: Bagging, Boosting, Stacking.
*   **[Clustering-Algorithms.md](Clustering-Algorithms.md)**: K-Means, DBSCAN.
*   **[Dimensionality-Reduction.md](Dimensionality-Reduction.md)**: PCA, t-SNE, UMAP.
*   **[Inference-Time-Compute.md](Inference-Time-Compute.md)**: System 2 Thinking.
*   **[Math-Reasoning.md](Math-Reasoning.md)**: CoT, ToT.
*   **[Knowledge-Graphs.md](Knowledge-Graphs.md)**: Structured knowledge & GraphRAG.

## 13. Safety, Ethics & Society
*   **[AI-Safety-Security.md](AI-Safety-Security.md)**: General security concepts.
*   **[Adversarial-Attacks.md](Adversarial-Attacks.md)**: Prompt Injection, Jailbreaking, Data Poisoning, and Evasion (FGSM).
*   **[Direct-Preference-Optimization.md](Direct-Preference-Optimization.md)**: **DPO**. Aligning models directly on preference data without training a separate Reward Model.
*   **[Watermarking-AI-Content.md](Watermarking-AI-Content.md)**: Techniques for detecting and tagging AI-generated text/images (C2PA, SynthID).
*   **[RLHF-Alignment.md](RLHF-Alignment.md)**: Aligning models with human values.
*   **[Constitutional-AI.md](Constitutional-AI.md)**: **RLAIF**. Using AI feedback (based on a constitution of principles) to supervise other AIs, scaling alignment beyond human labeling.
*   **[AI-Ethics-Fairness.md](AI-Ethics-Fairness.md)**: Bias mitigation.
*   **[Privacy-Preserving-AI.md](Privacy-Preserving-AI.md)**: Differential Privacy, Homomorphic Encryption.
*   **[Privacy-Attacks-and-Defenses.md](Privacy-Attacks-and-Defenses.md)**: Membership Inference, Model Inversion, and DP-SGD.
*   **[AI-Governance.md](AI-Governance.md)**: NIST AI RMF, ISO 42001.
*   **[EU-AI-Act.md](EU-AI-Act.md)**: European AI regulation.
*   **[Copyright-and-AI.md](Copyright-and-AI.md)**: Fair Use, ownership.
*   **[Deepfakes-and-Misinformation.md](Deepfakes-and-Misinformation.md)**: Detection and impact.
*   **[Sustainable-AI.md](Sustainable-AI.md)**: Green AI, carbon footprint.

## 14. Business & Strategy
*   **[AI-Maturity-Models.md](AI-Maturity-Models.md)**: Organizational readiness.
*   **[Build-vs-Buy.md](Build-vs-Buy.md)**: Strategic decision framework.
*   **[Sovereign-AI.md](Sovereign-AI.md)**: National AI infrastructure.
*   **[AI-Product-Management.md](AI-Product-Management.md)**: Managing the lifecycle of AI products, from ideation to monitoring.
*   **[AI-Cost-Modeling.md](AI-Cost-Modeling.md)**: Economics of AI. Token costs, GPU hours, and Total Cost of Ownership (TCO).
*   **[Open-Source-vs-Closed-Source.md](Open-Source-vs-Closed-Source.md)**: Strategic trade-offs between proprietary APIs and open-weights models.
*   **[AI-Risk-Management.md](AI-Risk-Management.md)**: Identifying and mitigating operational, reputational, and legal risks.

## 15. Emerging Frontiers
*   **[Artificial-General-Intelligence.md](Artificial-General-Intelligence.md)**: **AGI**.
*   **[Brain-Computer-Interfaces.md](Brain-Computer-Interfaces.md)**: **BCI**. Neuralink.
*   **[Digital-Twins.md](Digital-Twins.md)**: Virtual replicas.
*   **[Embodied-Cognition.md](Embodied-Cognition.md)**: Intelligence requiring a body.
*   **[Space-AI.md](Space-AI.md)**: Satellite imagery, autonomous rovers, astronomy.
*   **[Climate-AI.md](Climate-AI.md)**: Weather forecasting, climate modeling, energy optimization.

## 16. Agentic Workflows
*   **[Agentic-Workflows.md](Agentic-Workflows.md)**: ReAct, Plan-and-Solve.
*   **[AI-Agent-Frameworks.md](AI-Agent-Frameworks.md)**: Tools for building agents. AutoGen, CrewAI, LangGraph.
*   **[Multi-Agent-Collaboration.md](Multi-Agent-Collaboration.md)**: Architectures for multiple agents working together (Hierarchical, Round-Robin).
*   **[Tool-Use-Patterns.md](Tool-Use-Patterns.md)**: Function calling, API integration, and how agents interact with the world.
*   **[Agent-Memory-Architectures.md](Agent-Memory-Architectures.md)**: Short-term vs. Long-term memory, Episodic memory, and Vector stores.
*   **[Cognitive-Architectures.md](Cognitive-Architectures.md)**: Systems inspired by human cognition (Soar, ACT-R) applied to modern AI agents.
*   **[Reflection-and-Self-Correction.md](Reflection-and-Self-Correction.md)**: Agents critiquing their own output to improve quality (Self-Refine).
*   **[Planning-Algorithms-for-Agents.md](Planning-Algorithms-for-Agents.md)**: Tree of Thoughts (ToT), Graph of Thoughts (GoT), and A* search.
*   **[Memory-Stream.md](Memory-Stream.md)**: The architecture from "Generative Agents" (Simulacra) using recency, importance, and relevance.

## 17. Data Engineering
*   **[Data-Quality-for-AI.md](Data-Quality-for-AI.md)**: Testing and validation.
*   **[Data-Labeling.md](Data-Labeling.md)**: Strategies for annotating data. Manual, Semi-Supervised, and Weak Supervision (Snorkel).
*   **[Feature-Engineering.md](Feature-Engineering.md)**: Transforming raw data into model inputs. One-Hot, Embeddings, Scaling.
*   **[Data-Augmentation.md](Data-Augmentation.md)**: Mixup, CutMix.
*   **[Active-Learning.md](Active-Learning.md)**: Efficient labeling.
*   **[Curriculum-Learning.md](Curriculum-Learning.md)**: Easy-to-hard training.
*   **[Online-Learning.md](Online-Learning.md)**: Streaming updates.
*   **[Transfer-Learning.md](Transfer-Learning.md)**: Domain Adaptation.
*   **[Multi-Task-Learning.md](Multi-Task-Learning.md)**: Generalization.
*   **[Knowledge-Distillation.md](Knowledge-Distillation.md)**: Teacher-Student models.
*   **[Efficient-Fine-Tuning.md](Efficient-Fine-Tuning.md)**: **PEFT**. LoRA, QLoRA.

## 18. Frameworks & Standards
*   **[PyTorch.md](PyTorch.md)**: Dynamic graphs.
*   **[TensorFlow.md](TensorFlow.md)**: The production-grade framework. Static graphs, Keras, and TFX.
*   **[JAX.md](JAX.md)**: Functional high-performance computing.
*   **[Scikit-Learn.md](Scikit-Learn.md)**: The standard for classical ML algorithms.
*   **[LangChain.md](LangChain.md)**: LLM orchestration.
*   **[ONNX.md](ONNX.md)**: Interoperability standard.
*   **[Evaluation-Metrics.md](Evaluation-Metrics.md)**: Perplexity, BLEU, ROUGE.
*   **[LLM-Benchmarks.md](LLM-Benchmarks.md)**: Standardized tests for models. MMLU, GSM8K, HumanEval, Chatbot Arena.
*   **[LLM-as-a-Judge.md](LLM-as-a-Judge.md)**: Using strong models (GPT-4) to evaluate weaker models (AlpacaEval, MT-Bench).

## 19. Alternative Paradigms & Learning Strategies
*   **[Neurosymbolic-AI.md](Neurosymbolic-AI.md)**: Combining neural networks with symbolic logic and reasoning (Logic Tensor Networks).
*   **[Spiking-Neural-Networks.md](Spiking-Neural-Networks.md)**: **SNNs**. Biologically plausible, event-driven models that use spikes instead of continuous values.
*   **[Hyperdimensional-Computing.md](Hyperdimensional-Computing.md)**: **HDC**. Computing with large random vectors, offering robustness and efficiency.
*   **[Evolutionary-Strategies.md](Evolutionary-Strategies.md)**: **ES**. Optimization algorithms that don't rely on backpropagation (Neuroevolution, NEAT).
*   **[Federated-Learning.md](Federated-Learning.md)**: Training models across decentralized devices while keeping data local (Privacy-Preserving).
*   **[Self-Supervised-Learning.md](Self-Supervised-Learning.md)**: **SSL**. Learning from unlabeled data via pretext tasks (Contrastive Learning, MAE).
*   **[Energy-Based-Models.md](Energy-Based-Models.md)**: **EBMs**. Learning an energy function where low energy corresponds to high probability states.
*   **[Meta-Learning.md](Meta-Learning.md)**: "Learning to Learn". Algorithms that learn how to adapt quickly to new tasks (MAML).

## 20. Advanced Reinforcement & Learning Paradigms
*   **[Hierarchical-Reinforcement-Learning.md](Hierarchical-Reinforcement-Learning.md)**: **HRL**. Decomposing complex tasks into sub-goals (Options Framework).
*   **[Offline-Reinforcement-Learning.md](Offline-Reinforcement-Learning.md)**: Learning policies from static datasets without interacting with the environment.
*   **[Imitation-Learning.md](Imitation-Learning.md)**: Learning by observing a demonstrator (Behavior Cloning).
*   **[Inverse-Reinforcement-Learning.md](Inverse-Reinforcement-Learning.md)**: **IRL**. Inferring the reward function from observed behavior.
*   **[Zero-Shot-Learning.md](Zero-Shot-Learning.md)**: Recognizing classes not seen during training using semantic attributes.
*   **[One-Shot-Learning.md](One-Shot-Learning.md)**: Learning from a single example (Siamese Networks).

## 21. Scientific & Implicit Architectures
*   **[Physics-Informed-Neural-Networks.md](Physics-Informed-Neural-Networks.md)**: **PINNs**. Solving partial differential equations (PDEs) using neural networks.
*   **[Deep-Equilibrium-Models.md](Deep-Equilibrium-Models.md)**: **DEQs**. Finding fixed points of a layer instead of stacking finite layers (Infinite depth).
*   **[Normalizing-Flows.md](Normalizing-Flows.md)**: Invertible neural networks that map complex distributions to simple ones (Exact Likelihood).
*   **[Neural-Cellular-Automata.md](Neural-Cellular-Automata.md)**: **NCA**. Self-organizing systems that learn local update rules to form global patterns.

## 22. Advanced Theoretical Frameworks
*   **[Optimal-Transport.md](Optimal-Transport.md)**: **OT**. The mathematics of moving probability distributions (Wasserstein Distance, Earth Mover's Distance).
*   **[Conformal-Prediction.md](Conformal-Prediction.md)**: A framework for quantifying uncertainty with rigorous statistical guarantees.
*   **[Predictive-Coding.md](Predictive-Coding.md)**: A neuroscience-inspired theory where the brain constantly generates predictions and updates based on errors.
*   **[Graph-Transformers.md](Graph-Transformers.md)**: Applying the Transformer architecture to graph-structured data, overcoming GNN limitations (Oversmoothing).
