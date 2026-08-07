# Discount Factor as a Regularizer in Reinforcement Learning

## Code replication

This project reproduces and extends “Discount Factor as a Regularizer in Reinforcement Learning”
by Amit, Meir and Ciosek. The paper distinguishes the evaluation discount, which defines the task
objective, from the guidance discount used during learning. Reducing the guidance discount can
be rewritten as a quadratic activation regularizer on the estimated value function, with an explicit
relationship to L2 regularization under linear or tabular representations.
The project reviews and partially reproduces the paper’s tabular and continuous-control experiments,
focusing on limited-data regimes, non-uniform state distributions and mixing properties. It also
applies the same idea to Windy Gridworld and MountainCar. The Windy Gridworld extension
compares a baseline, discount-based regularization and explicit quadratic shrinkage, measuring
learning returns, greedy performance, value magnitude and action-value variance. The MountainCar
extension uses semi-gradient SARSA with tile coding and Proposition-1 reward and learning-rate
adjustments.

A report of the paper and both the orginal and new experiments can be consulted.

**Original paper :**
```bibtex
@inproceedings{amit2020discount,
  title={Discount Factor as a Regularizer in Reinforcement Learning},
  author={Amit, Ron and Meir, Ron and Ciosek, Kamil},
  booktitle={International Conference on Machine Learning},
  pages={269--278},
  year={2020},
  organization={PMLR}
}
```

**Original code:** [GitHub - Discount_as_Regularizer](https://github.com/...)

**Algoritms used:**
- TD3: [Fujimoto et al., 2018](https://arxiv.org/abs/1802.09477)
- LSTD: [Bradtke & Barto, 1996](https://ieeexplore.ieee.org/document/548471)

**Technologies and methods**

Python, NumPy, Matplotlib, Gymnasium, tabular reinforcement learning, TD(0), LSTD, SARSA, Q-learning,
semi-gradient methods, tile coding, TD3, confidence intervals and multi-seed evaluation.


This project has been released un MIT licence. See `LICENSE` for more details.

The original code is property of the authors (Amit et al., 2020).
