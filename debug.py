from InstructorEmbedding import INSTRUCTOR
model = INSTRUCTOR('hkunlp/instructor-xl')
# sentence = "3D ActionSLAM: wearable person tracking in multi-floor environments"
# instruction = "Represent the Science title:"
# embeddings = model.encode([[instruction,sentence]])
# print(embeddings)

from sklearn.metrics.pairwise import cosine_similarity
# sentences_a = [['Represent the Science sentence: ','Parton energy loss in QCD matter'],
#                ['Represent the Financial statement: ','The Federal Reserve on Wednesday raised its benchmark interest rate.']]
# sentences_b = [['Represent the Science sentence: ','The Chiral Phase Transition in Dissipative Dynamics'],
#                ['Represent the Financial statement: ','The funds rose less than 0.5 per cent on Friday']]
sentences_a = 'Represent the Science sentence: '
sentences_b = 'Represent the Science sentence: '
embeddings_a = model.encode(sentences_a).reshape(1, -1)
embeddings_b = model.encode(sentences_b).reshape(1, -1)
similarities = cosine_similarity(embeddings_a,embeddings_b)
print(similarities)
