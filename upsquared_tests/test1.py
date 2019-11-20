import mraa
import time

gpio_1 = mraa.Gpio(24)
gpio_1.dir(mraa.DIR_OUT)

print("[+] Inicializado")
time.sleep(2)

print("Led on")
gpio_1.write(1)

time.sleep(1)

print("Led off")
gpio_1.write(0)


print("bye")

