# Overview
本解决方案通过RAGAs评价框架的AnswerSimilarity评价指标,对bedrock中不同LLM+embedding模型组合进行评分,为客户提供最佳模型选择建议。同时基于用户提供的QA对生成新QA对,通过专家评估对answer进行排序,为企业构建基于RAG技术的知识库提供参考。解决方案部署在EKS之上，用户可以将其集成到自己的EKS环境内。

# Service
使用到的服务有EC2, Bedrock, EKS, S3, Cloud9, Opensearch serverless,dynamodb, ECR, Lambda, Cognito
# Function
模型评分：用户可以参考此结果从众多bedrock提供的模型中选择表现较好的模型  
专家评估：通过领域专家对生成的qa对进行打分，生成更高质量的qa对  
chatbot：使用高质量qa对进行chatbot的构建，从而更好的在企业内部落地  
# Page
## main page
﻿
![截屏2024-04-15 09 46 30](https://github.com/epiphany97/RAG-EVA/assets/73279725/e10b7f5e-cd27-4a9e-b11b-183beceebdbf)
# Usage
1、选择用于embedding模型，确定后点击save  
2、选择用于构建知识库的文件，可以是pdf,txt,.html,doc/docx,.csv,.xls/.xlsx格式；等到显示知识库创建成功后，进行下一步  
<img width="787" alt="Image55" src="https://github.com/epiphany97/RAG-EVA/assets/73279725/17e0e30f-37c3-4082-bb05-1fd7d79ac590">

3、选择用于RAG的模型，选择后点击“submit”按钮。选择qa文件，并点击上传qa文件，等到新的qa文件生成之后，再进行下一步。  
![Image44](https://github.com/epiphany97/RAG-EVA/assets/73279725/e5fab562-fb71-4bb5-8a13-b950a36e75ca)

4、选择左侧第一个选项栏：模型评估，到计算结果准备好之后，可以看到  
![Image33](https://github.com/epiphany97/RAG-EVA/assets/73279725/7056f310-ebdf-4103-8ddd-0c78bbffec7d)

5、选择左侧第二个选项栏：专家标注  


![截屏2024-04-15 09 46 30](https://github.com/epiphany97/RAG-EVA/assets/73279725/298a78a3-df0b-4aa4-aeeb-173fe4690446)
用户可以对所有的qa对进行标注排序，将最适合当前问题的答案记录下来。
当所有问题标注完成后，可以在dataset栏进行下载到本地

![Image2](https://github.com/epiphany97/RAG-EVA/assets/73279725/f6e44842-13a3-45a5-9cb6-02cd17afb9d1)
6、选择左侧第三个选项栏：chatbot
通过在Mode中进行选择，可以选择使用RAG模式，或者是使用T2T模式，Text2Text模式使用claude-instant作为llm，通过提问，用户得到的答案不经过RAG。RAG模式是将RHLF得到的优质QA对用来构建chatbot，可以看到经过RAG后的回答更精确。
<img width="1343" alt="截屏2024-04-14 22 08 46" src="https://github.com/epiphany97/RAG-EVA/assets/73279725/6ad3fba0-9151-4748-a902-6541e54eb3b9">
<img width="1407" alt="截屏2024-04-14 22 09 37" src="https://github.com/epiphany97/RAG-EVA/assets/73279725/c04995a6-fe54-42f9-8183-feb24dd70164">

# Reference
https://github.com/explodinggradients/ragas  
https://github.com/aws-samples/amazon-bedrock-workshop/blob/main/02_KnowledgeBases_and_RAG/0_create_ingest_documents_test_kb.ipynb  
https://aws.amazon.com/cn/blogs/containers/build-a-multi-tenant-chatbot-with-rag-using-amazon-bedrock-and-amazon-eks/  
https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/bedrock-runtime#code-examples  
https://docs.streamlit.io/develop/api-reference  

