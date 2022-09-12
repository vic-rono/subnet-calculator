import random
import sys


def subnet_calc():
    try:

        # Checking IP address validity
        while True:
            ip_addy = input("Enter Your IP address: ")

            # Checking octets/splitting the octets i.e 192.168.1.0
            a = ip_addy.split('.')
            # print a
            if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and \
                    (int(a[0]) != 169 or int(a[1]) != 254) and (
                    0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
                break
            # if statement to check whether the ipaddress(a) is valid and meet the following conditions: a should
            # have 4 elements, a[0] should be an integer a[0]  should be between 1 an  223 because i need it to be a
            # unicast address exclusively because 223 onwards are multicast addresses and those i can tell you are
            # experimental. a[0] 127 are reserved for loopback IPv4 addresses used for testing and will not be
            # included 169 and 254 in a[0][1] are reserved for dhcp servers to be exempted !=
            else:
                print("IP address is INVALID! Please re-enter!")
                continue

        masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]

        # Checking Subnet Mask validity
        while True:
            subnet_mask = input("Enter Your subnet mask: ")

            # Checking octets
            b = subnet_mask.split('.')
            # validating the subnet mask
            if (len(b) == 4) and (int(b[0]) == 255) and (int(b[1]) in masks) and (int(b[2]) in masks) and (
                    int(b[3]) in masks) and (int(b[0]) >= int(b[1]) >= int(b[2]) >= int(b[3])):
                break
            # b should have 4 octets
            # b[0] first octet have should have 255 and others 
            # ensuing octets should be in masks = [] 
            else:
                print("The subnet mask is INVALID! Please retry!")
                continue

        # Convert mask to binary string
        mask_padded = []  # stored as an element in binary format
        mask_decimal = subnet_mask.split(".")

        for octet_index in range(0, len(mask_decimal)):

            binary_octet = bin(int(mask_decimal[octet_index])).split("b")[1]  # bin converts it to a binary presentation
            # print binary_octet

            if len(binary_octet) == 8:
                mask_padded.append(binary_octet)

            elif len(binary_octet) < 8:
                binary_octet_padded = binary_octet.zfill(
                    8)  # during conversion if the bits are less zfill adds 0s that are lacking to achieve a 32-bit octet
                mask_padded.append(binary_octet_padded)

        # print octets_padded

        decimal_mask = "".join(mask_padded)  # joins e.g255.255.255.0 => 11111111111111111111111100000000
        # print decimal_mask

        # Counting host bits in the mask and calculating number of hosts/subnet
        zeros = decimal_mask.count("0")  # returns the number of host bits(0)
        ones = 32 - zeros
        hosts = abs(2 ** zeros - 2)  # abs return positive value for mask /32 #2^x-2

        # print zeros
        # print ones
        # print hosts

        # Getting the wildcard mask based on the subnet mask
        wildcard_octets = []
        for w_octet in mask_decimal:
            wild_octet = 255 - int(w_octet)
            wildcard_octets.append(str(wild_octet))

        # print wildcard_octets

        wildcard_mask = ".".join(wildcard_octets)
        # print wildcard_mask

        # Convert IP to binary string
        octets_padded = []
        octets_decimal = ip_addy.split(".")

        for octet_index in range(0, len(octets_decimal)):

            binary_octet = bin(int(octets_decimal[octet_index])).split("b")[1]

            if len(binary_octet) < 8:
                binary_octet_padded = binary_octet.zfill(8)
                octets_padded.append(binary_octet_padded)

            else:
                octets_padded.append(binary_octet)

        binary_ip = "".join(octets_padded)

        # print binary_ip   #Example: for 192.168.2.100 => 11000000101010000000001001100100

        network_binary = binary_ip[:ones] + "0" * zeros

        broadcast_binary = binary_ip[:ones] + "1" * zeros

        net_octets = []
        for octet in range(0, len(network_binary), 8):
            net_octet = network_binary[octet:octet + 8]
            net_octets.append(net_octet)

        net_address = []
        for each_octet in net_octets:
            net_address.append(str(int(each_octet, 2)))

        network_address = ".".join(net_address)

        bst_octets = []
        for octet in range(0, len(broadcast_binary), 8):
            bst_octet = broadcast_binary[octet:octet + 8]
            bst_octets.append(bst_octet)

        brst_address = []
        for each_octet in bst_octets:
            brst_address.append(str(int(each_octet, 2)))

        broadcast_address = ".".join(brst_address)

        # Results for selected IP/mask

        print("Network address is: ", network_address)
        print("Broadcast address is: ", broadcast_address)
        print("Number of valid hosts per subnet: ", hosts)
        print("Wildcard mask:  ", wildcard_mask)
        print("Mask bits: ", ones)

        # Generation of random IP in subnet
        while True:
            generate = input("Generate random ip address? (y/n)")

            if generate == "y":
                generated_ip = []

                # Obtain available IP address in range, based on the difference between octets in broadcast address
                # and network address
                for x, oct_bst in enumerate(brst_address):

                    for y, oct_net in enumerate(net_address):

                        if x == y:
                            if oct_bst == oct_net:
                                # Add identical octets to the generated_ip list
                                generated_ip.append(oct_bst)
                            else:
                                # Generate random number(s) from within octet intervals and append to the list
                                generated_ip.append(str(random.randint(int(oct_net), int(oct_bst))))

                my_address = ".".join(generated_ip)

                print("Your Random IP address is: ", my_address)
                print("\n")
                continue

            else:
                print("Peace out....IP town!!!\n")
                break

    except KeyboardInterrupt:
        print("\n\nExiting...\n")
        sys.exit()
        # handles program exit during run time


subnet_calc()
