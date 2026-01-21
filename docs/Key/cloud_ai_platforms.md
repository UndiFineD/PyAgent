# Cloud AI Platforms

While you can train models on a local GPU, enterprise AI requires scalable infrastructure. The "Big Three" cloud providers offer managed services to handle the entire ML lifecycle.

## AWS SageMaker
Amazon's fully managed machine learning service.
*   **SageMaker Studio**: A web-based IDE for ML.
*   **Autopilot**: AutoML capability to automatically build, train, and tune models.
*   **Data Wrangler**: Tool for data preparation and feature engineering.
*   **Inference**: Supports real-time endpoints, serverless inference, and asynchronous inference.
*   **Bedrock**: A serverless API to access foundation models (Claude, Titan, Llama 2) without managing infrastructure.

## Google Cloud Vertex AI
Google's unified AI platform, replacing the old AI Platform.
*   **Model Garden**: A library of foundation models (PaLM, Gemini, BERT) that can be tuned and deployed.
*   **AutoML**: Google's state-of-the-art AutoML for vision, text, and tabular data.
*   **TPU Integration**: Seamless access to Tensor Processing Units (TPUs) for massive scale training.
*   **BigQuery ML**: Allows you to create and execute ML models in BigQuery using standard SQL queries.

## Azure AI
Microsoft's portfolio of AI services.
*   **Azure Machine Learning (AML)**: The core platform for building, training, and deploying models. Strong integration with VS Code.
*   **Azure OpenAI Service**: Exclusive enterprise access to OpenAI's models (GPT-4, DALL-E 3) with Azure's security and compliance (VNETs, private endpoints).
*   **Cognitive Services**: Pre-built APIs for Vision, Speech, Language, and Decision (e.g., Anomaly Detector).

## Comparison
*   **AWS**: Most mature, vast ecosystem, but steep learning curve.
*   **GCP**: Best for "Big Data" and TPUs. Strongest research pedigree.
*   **Azure**: Best for enterprise integration (Office 365, Active Directory) and OpenAI access.
