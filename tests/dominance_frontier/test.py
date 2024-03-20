import sys
import os

from jsoncomment import JsonComment


thisDirPath = os.path.dirname(os.path.abspath(__file__))
codeDirPath = os.path.abspath(thisDirPath + "/../..")
sys.path.append(codeDirPath)


from typing import List
import ui

from dominance_frontier import DominanceFrontier


file_names: List[str] = ['dominance_frontier_1.json']


def run_test(file_name: str) -> None:
	ui.ColoredPrint(f'#c********************   #y{file_name}#c   ********************#rs')
	
	file_path: str = os.path.join(thisDirPath, file_name)
	df, info = DominanceFrontier.value_of(file_path).calculate()

	is_passed: bool = df == [set(), {1}, {7}, {7}, {6}, {6}, {7}, {1}]

	if is_passed:
		ui.ColoredPrint("#gTest passed!#rs")
		print(info)
	else:
		ui.ColoredPrint("#rTest FAILED.#rs")

	ui.ColoredPrint(f'\n#c**********************************************' + '*' * len(file_name) + '#rs\n')
	

if __name__ == '__main__':
	for file_name in file_names:
		run_test(file_name)
