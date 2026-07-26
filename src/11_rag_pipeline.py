from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from gigachat import GigaChat



# -------------------------
# Настройки
# -------------------------

COLLECTION_NAME = "mv85500"


GIGACHAT_KEY = "КЛЮЧ_ОТ_ГИГАЧАТА"



# -------------------------
# Модели
# -------------------------

embedding_model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)



qdrant = QdrantClient(
    path="../qdrant"
)



llm = GigaChat(
    credentials=GIGACHAT_KEY,
    verify_ssl_certs=False
)



# -------------------------
# Вопрос пользователя
# -------------------------
A = True
while A:
    question = input(
        "Введите вопрос: "
    )

    if question == "":
        A = False


    # -------------------------
    # 1. Embedding вопроса
    # -------------------------

    query_vector = embedding_model.encode(
        question,
        normalize_embeddings=True
    ).tolist()



    # -------------------------
    # 2. Поиск в Qdrant
    # -------------------------

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,

        query=query_vector,

        limit=5
    ).points



    # -------------------------
    # 3. Собираем контекст
    # -------------------------

    context = ""


    for i, result in enumerate(results):

        context += f"""
    Источник {i+1}
    
    {result.payload['text']}
    
    ---
    """



    # -------------------------
    # 4. Prompt для LLM
    # -------------------------

    prompt = f"""
    Ты технический ассистент по контроллеру MV85500.
    
    Отвечай только используя предоставленный контекст.
    
    Если информации нет в контексте, скажи:
    "В документации нет информации".
    
    Контекст:
    
    {context}
    
    
    Вопрос пользователя:
    
    {question}
    """



    # -------------------------
    # 5. Ответ GigaChat
    # -------------------------

    response = llm.chat(prompt)



    print("\nОтвет:")

    print(
        response.choices[0].message.content
    )



qdrant.close()