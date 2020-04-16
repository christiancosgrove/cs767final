import json
import matplotlib.pyplot as plt


results = json.load(open('results.json', 'r'))

for line in results:
    print(line)

    res = {}

    for key in line:
        if key[:4] == 'hits':
            res[int(key[5:])] = line[key]


    x, y = zip(*sorted(res.items(), key=lambda x: x[0]))
    plt.plot(x,y)

plt.title('Accuracy on COVID-QA eval set')
plt.legend([line['model'] for line in results])
plt.xlabel('topk')
plt.ylabel('hits')
plt.show()