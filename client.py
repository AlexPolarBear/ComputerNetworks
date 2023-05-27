import os
import socket
import struct
import sys
import click
import time


host = 'localhost'
port = 21
address = (host, port)

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
d = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


@click.command()
# @click.argument('user', default='TestUser', help='User name.')
# @click.argument('password', default=12345, help='Password for authentication user.')
def connect():
    """
    Create connection with server.
    """

    print("Sending server request...")
    try:
        print("Сonnection is available at 127.0.0.1 on the port 21.")
        d.connect(address)
        
        # d.send(b"AUTH TLS\r\n")
        # time.sleep(1)
        user = click.prompt("Enter the User Name", default="TestUser")
        d.send(f"USER {user}\r\n".encode())
        time.sleep(1)
        password = click.prompt("Enter the password", default=12345)
        d.send(f"PASS {password}\r\n".encode())
        time.sleep(1)
        # d.send(b"FEAT\r\n")
        # time.sleep(1)
        d.send(b"PWD\r\n")
        time.sleep(1)
        d.send(b"TIPE I\r\n")
        time.sleep(1)
        click.echo("Loggin successful. Waiting while enter the Passive Mode.")
    except:
        click.echo("Connection unsucessful. Make sure the server is online.")
        
    try:    
        d.send(b"PASV\r\n")
        time.sleep(1)
        data = d.recv(1024).decode()
        substrings = []
        split_str = data.split("(")
        for one in split_str[1:]:
            split_s = one.split(")")
            if len(split_s) > 1:
                substrings.append(split_s[0])
 
        substrings_str = "".join(substrings)
        host = ".".join(substrings_str.split(",")[:4])
        port = (int(substrings_str.split(",")[4]) << 8)
        port += int(substrings_str.split(",")[5])
        d.connect((host, port))
        time.sleep(3)
        click.echo("Connection sucessful.")
    except:
        click.echo("Connection sucessful.")


@click.command()
# @click.option('--list', help="return the list of files in directory")
def list():
    """
    Return list of files.
    """

    click.echo("Requesting files...")
    try:
        d.send(b"LIST\r\n")
        time.sleep(4)
    except:
        click.echo("Couldn't make server request. "
                   "Make sure a connection has been established.")
        return
    try:
        number_of_files = struct.unpack(i, d.recv(1024))[0]
        for i in range(int(number_of_files)):
            file_name_size = struct.unpack(i, d.recv(1024))[0]
            file_name = d.recv(file_name_size)
            file_size = struct.unpack(i, d.recv(1024))[0]
            click.echo(f"\t{file_name} - {file_size}b.")
            d.send(b"1")
            time.sleep(2)
        total_directory_size = struct.unpack(i, d.recv(1024))[0]
        click.echo(f"Total directory size: {total_directory_size}b.")
    except:
        click.echo("Couldn't retrieve listing.")
        return
    try:
        d.send(b"1")
        time.sleep(2)
    except:
        click.echo("Couldn't get final server confirmation.")
        return


@click.command()
# @click.argument('file_name')
def upload(file_name):
    """
    Upload a files.
    """

    click.echo(f"Uploading file: {file_name}...")
    try:
        content = open(file_name, "rb")
    except:
        click.echo("Couldn't open file. "
                   "Make sure the file name was entered correctly.")
        return
    
    try:
        d.send(b"UPLD\r\n")
        time.sleep(2)
    except:
        click.echo("Couldn't make server request. "
                   "Make sure a connection has bene established.")
        return
    
    try:
        d.send(struct.pack("h", sys.getsizeof(file_name)))
        time.sleep(2)
        d.send(file_name)
        time.sleep(2)
        d.send(struct.pack("i", os.path.getsize(file_name)))
        time.sleep(2)
    except:
        click.echo("Error sending file details.")
        return
    
    try:
        l = content.read(1024)
        click.echo("\nSending...")
        while l:
            d.send(l)
            time.sleep(2)
            l = content.read(1024)
        content.close()

        upload_time = struct.unpack("f", d.recv(1024))[0]
        upload_size = struct.unpack("i", d.recv(1024))[0]
        click.echo(f"\nSent file: {file_name}.\n"
                   f"Time elapsed: {upload_time}s.\nFile size: {upload_size}b.")
    except:
        click.echo("Error sending file.")
        return
    return


@click.command()
# @click.argument('file_name')
def download(file_name):
    """
    Download file by it name.
    """

    click.echo(f"Downloading file: {file_name}.")
    try:
        d.send(b"DWLD\r\n")
        time.sleep(2)
    except:
        click.echo("Couldn't make server request. "
                   "Make sure a connection has bene established.")
        return
    
    try:
        d.send(struct.pack("h", sys.getsizeof(file_name)))
        time.sleep(2)
        d.send(file_name)
        time.sleep(2)
        file_size = struct.unpack("i", d.recv(1024))[0]
        if file_size == -1:
            click.echo("File does not exist. "
                       "Make sure the name was entered correctly.")
            return
    except:
        click.echo("Error checking file.")
    
    try:
        d.send(b"1")
        time.sleep(2)
        output_file = open(file_name, "wb")
        bytes_recieved = 0
        click.echo("\nDownloading...")
        while bytes_recieved < file_size:
            l = d.recv(1024)
            time.sleep(2)
            output_file.write(l)
            bytes_recieved += 1024
        output_file.close()
        click.echo(f"Successfully downloaded {file_name}.")
        
        d.send(b"1")
        time_elapsed = struct.unpack("f", d.recv(1024))[0]
        click.echo(f"Time elapsed: {time_elapsed}s.\n"
                   f"File size: {file_size}b.")
    except:
        click.echo("Error downloading file.")
        return
    return


@click.command()
def quit():
    """
    Stop connection with server.
    """

    d.send(b"QUIT\r\n")
    time.sleep(2)
    d.close()
    click.echo("Server connection ended.")
    return


if __name__ == '__main__':
    click.echo("\nWelcome to the FTP client.\n"
               "Call one of the following functions:")
    time.sleep(0.5)
    click.echo("\tCONN\t\t: Connect to server\n"
          "\tUPLD file_path\t: Upload file\n"
          "\tLIST\t\t: List files\n"
          "\tDWLD file_path\t: Download file\n"
          "\tQUIT\t\t: Exit\n")
    while True:
        prompt = click.prompt("Enter a command")
        if prompt[:4].upper() == "CONN":
            connect(standalone_mode=False)
        elif prompt[:4].upper() == "UPLD":
            if len(prompt[5:]) == 0:
                file_path = click.prompt("Please enter path to the file")
                upload(file_path, standalone_mode=False)
            upload(prompt[5:], standalone_mode=False)
        elif prompt[:4].upper() == "LIST":
            list(standalone_mode=False)
        elif prompt[:4].upper() == "DWLD":
            if len(prompt[5:]) == 0:
                file_path = click.prompt("Please enter path to the file")
                upload(file_path, standalone_mode=False)
            download(prompt[5:], standalone_mode=False)
        elif prompt[:4].upper() == "QUIT":
            quit()
        else:
            click.echo("Command not recognised; please try again")
