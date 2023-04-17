from multiprocessing import Pool
import subprocess

def run_command(command):
    subprocess.Popen(command, shell=True)

if __name__ == '__main__':
    pool = Pool()
    pool.map(run_command, [
        'cd backend && npm start',
        'cd frontend && npm start'
    ])