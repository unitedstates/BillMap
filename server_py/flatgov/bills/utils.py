
def sort_bills_for_congress(our_list):
    # We go through the list as many times as there are elements
    for i in range(len(our_list)):
        # We want the last pair of adjacent elements to be (n-2, n-1)
        for j in range(len(our_list) - 1):
            if our_list[j][:3] < our_list[j+1][:3]:
                # Swap
                our_list[j], our_list[j+1] = our_list[j+1], our_list[j]
