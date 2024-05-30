import argparse
import json
import time
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from transformers import BertTokenizer, BertModel
import torch
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def cluster_and_visualize(corpus, batch_size=4, path="bert-cn",true_k = 8):
    # 加载预训练的BERT模型和分词器
    tokenizer = BertTokenizer.from_pretrained(path)
    model = BertModel.from_pretrained(path)

    # 将文本转换为嵌入向量，分批处理
    def get_embeddings_batch(texts, tokenizer, model, batch_size=1):
        embeddings = []
        for i in range(0, len(texts), batch_size):
            if isinstance(corpus[0], dict):
                batch = [item["content"] for item in texts[i:i + batch_size]]
            else:
                batch = texts[i:i + batch_size]
            encoded_input = tokenizer(batch, padding=True, truncation=True, return_tensors='pt')
            with torch.no_grad():
                output = model(**encoded_input)
            batch_embeddings = output.last_hidden_state[:, 0, :].numpy()
            embeddings.append(batch_embeddings)
        embeddings = np.vstack(embeddings)
        return embeddings

    # 获取嵌入向量
    start_time = time.time()
    embeddings = get_embeddings_batch(corpus, tokenizer, model, batch_size)
    end_time = time.time()
    print(f"1代码块执行时间: {end_time - start_time} 秒")
    # 使用K-means算法进行聚类
    true_k = true_k
    start_time = time.time()
    kmeans_model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    kmeans_model.fit(embeddings)
    end_time = time.time()
    print(f"2代码块执行时间: {end_time - start_time} 秒")

    # 将聚类结果添加到原始的JSON数据中
    for i, label in enumerate(kmeans_model.labels_):
        corpus[i]['Tag'] = f'Cluster {label}'

    # 根据Tag排序
    sorted_corpus = sorted(corpus, key=lambda x: x['Tag'])

    # 输出排序后的结果
    for item in sorted_corpus:
        print(item)

    with open("data_with_tags.json", 'w', encoding='utf-8') as file:
        json.dump(sorted_corpus, file, ensure_ascii=False, indent=4)
    # 输出聚类结果
    print("聚类结果：")
    print(kmeans_model.labels_)

    # 如果需要评估聚类的效果，可以使用轮廓系数
    print("轮廓系数：")
    print(silhouette_score(embeddings, kmeans_model.labels_))

    # 使用t-SNE进行降维
    tsne = TSNE(n_components=2, perplexity=4, learning_rate=10, n_iter=1000, random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings)

    # 可视化聚类结果
    plt.figure(figsize=(10, 8))
    labels = kmeans_model.labels_

    for i in range(true_k):
        plt.scatter(embeddings_2d[labels == i, 0], embeddings_2d[labels == i, 1], s=100, alpha=0.5, label=f'Cluster {i}')

    plt.xlabel('t-SNE 1')
    plt.ylabel('t-SNE 2')
    plt.legend()
    plt.title('BERT Embeddings Clustering')
    plt.show()

# 外部调用函数

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BERT Embeddings Clustering')
    parser.add_argument('--true_k', type=int, help='Number of clusters')
    parser.add_argument('--corpus_path', type=str, help='Path to the corpus JSON file')
    parser.add_argument('--model_path', type=str, help='Path to the model')
    args = parser.parse_args()

    with open(args.corpus_path, 'r', encoding='utf-8') as file:
        # 读取文件内容并转换为Python对象
        corpus = json.load(file)
        corpus = corpus[800:1600]
    cluster_and_visualize(corpus,true_k = args.true_k,path=args.model_path)