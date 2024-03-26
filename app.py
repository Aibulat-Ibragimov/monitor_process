import subprocess
import time


def monitor_process(
        command, output_file, restart_on_failure=False, kill_after_seconds=None
):
    """
    Мониторинг процесса, запись вывода в файл, перезапуск при неудачном
    завершении и завершение по прошествии времени.
    """

    while True:
        with open(output_file, 'a') as file:   # Запуск процесса и направление вывода в файл
            process = subprocess.Popen(
                command, shell=True, stdout=file, stderr=file
            )
            start_time = time.time()   # Время старта процесса

            while process.poll() is None:   # Цикл ожидания завершения процесса
                time.sleep(1)
                # Принудительное завершение процесса по прошествии времени
                if kill_after_seconds and time.time() - start_time > kill_after_seconds:
                    process.terminate()
                    break

            # Перезапуск процесса при неудачном завершении
            if restart_on_failure and process.returncode is not None and process.returncode != 0:
                file.write(
                    f"Process exited with return code {process.returncode}. Restarting...\n"
                )
                time.sleep(10)  # Пауза перед перезапуском
            else:
                break  # Прерывание цикла
