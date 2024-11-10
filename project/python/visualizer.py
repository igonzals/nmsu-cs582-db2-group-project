# add to dockerfile if needed
import matplotlib.pyplot as plt
import numpy as np

redis =  [0.1, 0.00329, .00172, 0.210]
sqlite = [0.1, 0.00383, .00108, 0.051]
query_name = ['Equality', 'Full-Text', 'Range', 'Aggregate']

x = np.arange(len(query_name))
width = 0.35
fig, ax = plt.subplots()
fig.tight_layout()
rects1 = ax.bar(x - width / 2, redis, width, label='Redis')
rects2 = ax.bar(x + width / 2, sqlite, width, label='Sqlite')

ax.set_ylabel('Average Runtime')
ax.set_title('Runtime per database')
ax.set_xticks(x)
ax.set_xticklabels(query_name)
ax.legend()

plt.show()
