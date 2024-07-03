import subprocess
import os
import time

def run_hh_ru_script():
    subprocess.run(["python", "hh-ru.py"])

def run_pars_upt_script():
    if os.path.exists("vacancies.json"):
        subprocess.run(["python", "pars-upt.py"])
    else:
        print("Файл vacancies.json не был создан. Процесс pars-upt.py не будет запущен.")

if __name__ == "__main__":
    run_hh_ru_script()
    run_pars_upt_script()
