from jsoncomment import JsonComment
from typing import List, Set, Dict, Tuple


class DominanceFrontier:
	@staticmethod
	def value_of(file_path):
		data = JsonComment().loadf(file_path)
	
		N: list(int) = []
		for i in data['N']:
			N.append(i)

		pred: list(set(int)) = []
		for pred_i in data['pred']:
			pred.append(set(pred_i))

		dom: list(set(int)) = []
		for dom_i in data['dom']:
			dom.append(set(dom_i))

		idom: list(int) = []
		for idom_i in data['idom']:
			idom.append(idom_i)

		return DominanceFrontier(N, pred, dom, idom)

	def __init__(self, N: List[int], pred: List[Set[int]], dom: List[Set[int]], idom: int) -> None:
		self.N: list(int) = N
		self.pred: list(set(int)) = pred
		self.dom: list(set(int)) = dom
		self.idom: list(set(int)) = idom

	def calculate(self, ) -> Tuple[List[Set[int]], str]:
		df: List[Set[int]] = []
		info: str = ''

		n: int
		for n in self.N:
			df.append(set())

		info += f'1) initialize: df = {df}\n'

		info += f'2)\n'

		n: int
		for n in self.N:
			if len(self.pred[n]) <= 1:
				info += f'- n = {n} - skip, because len(pred[n]) = {len(self.pred[n])} <= 1\n'

				continue

			info += f'- n = {n}:\n'

			p: int
			for p in self.pred[n]:
				r: int = p

				while r != self.idom[n]:
					info += f'-\t r = {r}\n'

					df[r] = df[r] | {n}

					info += f'-\t df[{r}] = {df[r]}\n'
					info += f'-\n'

					r = self.idom[r]


		info += f'3) df = {df}'

		return df, info
