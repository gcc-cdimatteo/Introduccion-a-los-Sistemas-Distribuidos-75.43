import matplotlib.pyplot as plt

CAMPUS = "campusgrado.fi.uba.ar"
CAMPUS_FILENAME = "campus"
GOOGLE = "google.com.ar"
GOOGLE_FILENAME = "google"

PATH = "/Users/cdimatteo/Documents/FIUBA/Introducción a los Sistemas Distribuidos (75.43)/ping/"
PING_RESULT_LENGTH = 14
STATICS_RESULT_LENGTH = 15
DATE_INITIAL_POS = 0
DATE_FINAL_POS = 2
HOUR_POS = 3
BYTES_RECV_POS = 6
IP_ADDRESS_POS = 9
ICMP_SEQ_POS = 10
TTL_POS = 11
TIME_POS = 12

def is_ping_result(line: list) -> bool:
    return len(line) == PING_RESULT_LENGTH

def get_ip_address(line: list) -> str:
    return line[IP_ADDRESS_POS].rstrip(':')

def add_result(line: list, output: dict) -> None:
    icmp_seq = int(line[ICMP_SEQ_POS].lstrip("icmp_seq="))
    ttl = int(line[TTL_POS].lstrip("ttl="))
    time = float(line[TIME_POS].lstrip("time="))
    bytes_recv = int(line[BYTES_RECV_POS])

    output[icmp_seq] = [ttl, time, bytes_recv, line[HOUR_POS]]

def read_output(path: str) -> tuple[str, dict]:
    with open(path) as f:
        content = f.readlines()
        
    output = {}
    ip_address = ""
    
    for line in content:
        line = line.rstrip().split(' ')
        if not is_ping_result(line): continue
        if ip_address == "": ip_address = get_ip_address(line)
        add_result(line, output)
    
    return ip_address, output

def plot_output(x, y, host_pinged, file_name) -> None:
    plt.clf()
    plt.figure(figsize=(11,8))
    plt.grid(True)
    plt.hist(y, bins=1000, alpha=1, log=True, color="hotpink")
    plt.title(f"Distribución de PING a {host_pinged} en Escala Lineal")
    plt.autoscale(True)
    plt.savefig(PATH + file_name + "_lineal")

    plt.clf()
    plt.figure(figsize=(11,8))
    plt.grid(True)
    plt.loglog(x, y, color="mediumorchid")
    plt.title(f"Distribución de PING a {host_pinged} en Escala Log-Log")
    plt.autoscale(True)
    plt.savefig(PATH + file_name + "_loglog")

def plot_both_log_log(x_campus, y_campus, x_google, y_google) -> None:
    file_path = PATH + CAMPUS_FILENAME + "_" + GOOGLE_FILENAME

    plt.clf()
    plt.figure(figsize=(9,6))
    plt.grid(True)
    plt.loglog(x_campus, y_campus, color="darkorange", label="campus")
    plt.loglog(x_google, y_google, color="lightseagreen", label="google")
    plt.title(f"Distribución de PING a {CAMPUS} y {GOOGLE} en Escala Log-Log")
    plt.autoscale(True)
    plt.legend()
    plt.savefig(file_path + "_loglog")


def get_x_y(output):
    y = list(map(lambda l: l[1], output.values()))
    x = range(len(y))
    return x, y

def main():
    # output = {icmp_seq: [ttl, time_ms, bytes_recv, date]}
    
    ip_address, output_campus = read_output(PATH + CAMPUS_FILENAME + ".txt")
    x_campus, y_campus = get_x_y(output_campus)
    plot_output(x_campus, y_campus, CAMPUS, CAMPUS_FILENAME)

    ip_address, output_google = read_output(PATH + GOOGLE_FILENAME + ".txt")
    x_google, y_google = get_x_y(output_google)
    plot_output(x_google, y_google, GOOGLE, GOOGLE_FILENAME)

    plot_both_log_log(x_campus, y_campus, x_google, y_google)

main()