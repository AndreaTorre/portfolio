Methodological reproduction of an unsupervised EA-net pipeline for lignocellulolytic enzyme-cocktail
optimization. The project combines substrate and enzyme embeddings, attention, residual features,
contrastive representation learning and clustering with KMeans, agglomerative clustering and BIRCH.

## The work

This project reproduces the methodological components of “A New Paradigm in Lignocellulolytic En-
zyme Cocktail Optimization”. The dataset contains all 2,310 combinations between 77 lignocellulosic
substrates and 30 enzyme cocktails. Substrates are represented through composition and structural
variables, while each cocktail is described by four enzyme codes.
The EA-net-inspired encoder combines feature embeddings, attention between substrate components
and enzymes, and a residual branch preserving the original variables. Contrastive learning is used to 
obtain robust representations without sugar-yield labels. The resulting 96-dimensional embeddings
are clustered using KMeans, agglomerative clustering and BIRCH.
The available experimental sugar-yield labels from the original study were not accessible, so the project
reproduces the representation-learning and clustering methodology but does not claim biological
validation of high-performing cocktails. The repository also documents a cluster-label alignment
issue that must be resolved before majority-vote consensus clustering.

## Technologies and methods

Python, NumPy, Pandas, TensorFlow/Keras, attention mechanisms, residual connections, contrastive learning,
projection heads, KMeans, agglomerative clustering, BIRCH, silhouette analysis and adjusted Rand index.
