import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
import matplotlib.pyplot as plt
from myConvexHull import ConvexHull

print("Convex Hull for Visualization of Dataset Linear Separability Tests")

print("""
    1. Iris
    2. Wine
    3. Breasts Cancer
    """)

datanum = int(input("Masukkan dataset yang ingin diuji: "))
if datanum == 1:
    data = datasets.load_iris()
elif datanum == 2:
    data = datasets.load_wine()
elif datanum == 3:
    data = datasets.load_breast_cancer()
else:
    print("Input salah!")

for i in range(len(data.feature_names)):
    print(f'{i + 1}. {data.feature_names[i]}')
print("\n")

x = int(input("Pilih variabel pada sumbu-x: ")) - 1
y = int(input("Pilih variabel pada sumbu-y: ")) - 1

df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = pd.DataFrame(data.target)

plt.figure(figsize=(10, 6))
colors = ['b', 'r', 'g']

plt.title(
    f'{data.feature_names[x].capitalize()} vs {data.feature_names[y].capitalize()}')
plt.xlabel(data.feature_names[x])
plt.ylabel(data.feature_names[y])

for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:, [x, y]].values
    hull = ConvexHull(bucket)
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
    for simplex in hull.simplices:
        plt.plot(bucket[simplex, 0], bucket[simplex, 1], colors[i])

plt.legend()
plt.show()

print("Thank you!!!")
