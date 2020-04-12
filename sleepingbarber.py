import threading, random, time
from threading import Lock
from queue import Queue

condition = threading.Condition()

print("Welcome to Chloe's Barber shop!\n\n") # print statement to say that my barber shop is opened
print("We have 3 of the best barbers available with 15 seats in our waiting room!\n\n")


def wait():
    time.sleep(0.1 * random.randint(1,3)) # a function that calculates wait time 


class Barber(threading.Thread):
    def __init__(self, queue, barber):
        threading.Thread.__init__(self)
        self.queue = queue # uses a queue to put the barbers into
        self.barber = barber # name of barber
        self.asleep = True # before program starts, barber is set to being asleep automatically

    def schedule(self): # Used to check for customers, if there are none, barber goes to sleep.
        if self.queue.empty():
            self.asleep = True # if the queue is empty, barber will stay asleep
            print("Barber {:s} is asleep.".format(self.barber))
        else:
            self.asleep = False # if the queue is empty babrer will wake up
            print("Barber {:s} is awake.".format(self.barber))


    def run(self):
        while True: 
            condition.acquire() #acquires the lock
            while self.queue.empty(): # while the queue is empty
                condition.wait() # waits for customer to come in 
            self.schedule() # refers back to the schedule function and sets the appropatie sleeping schedule and print statment
            condition.release() # the lock is released for next barber to use (wake up), I used locks so that one barber wakes up at a time when a customer comes in.
            customer1 = self.queue # gets customer on queue
            customer1.get().hair_service() # gets customer and refers to my hair_service function in customer class
            customer1.task_done() # says that the previous enqueued task has be completeted
            print("Barber {:s} has finished the hair service.".format(self.barber)) 
            print("Barber {:s} is now going for a nap\n".format(self.barber))

            if self.queue.empty(): # if the queue is empty the program will break.
                break

class Customer(threading.Thread):   # Customer is a subclass of threading.Thread superclass
    def __init__(self, queue,number):
        threading.Thread.__init__(self)
        self.queue = queue # a queue is used for the customers that will enter my shop.
        self.number = number # the number that is assigned to a customer when they enter my shop.

    def run(self):
        condition.acquire() # acquires the lock
       
        if self.queue.full(): #if the queue is full, the print statement will be printed
            print("Oooooh the waiting room is full, Customer {:d} has left shop".format(self.number))
            condition.notify(1) #signals the condition.wait in the barber class
            condition.release() # releases the lock that the next lock acquire will use in the barber class 
        else:
            condition.notify(1) # signals the condition.wait in the barber class to start if the queue isnt full
            condition.release() # releases the lock that the next lock acquire will use use in the barber class
   
    def hair_service(self):
        print("Customer {:d} is getting their haircut".format(self.number)) # when this function is called it will print the print statment
        cut = random.randint(1, 2) # will calculate a random number from the numbers given for the cut variable
        time.sleep(cut) # will sleep for the time that the cut variable calculates
        print("Customer {:d}'s haircut has finished".format(self.number)) # prints that the haircut has finished

def main():
    barbers = ["Harry Styles", "Justin Bieber", "Niall Horan"] # names of the barbers in my shop
    queue = Queue(maxsize=15) # queue for the customers which is given the maxsize of 15
    total_cus = [i for i in range(1,40)] # creates a list of numbers from the range 1 to 40 ( so 1 to 39)
    total_customers = 0
    rejected_customers = 0

    barbers_threads = [] # a list that i use to append the barber threads to
    for barb in barbers: # a for loop that takes a barber name from the barbers list and adds the name to the barber thread
        b = Barber(queue, barb)
        barbers_threads.append(b) # barber thread is appended to
        b.start()
   
    customer_threads = []
    for c in total_cus:
        c = Customer(queue,c)
        customer_threads.append(c) # appending customer thread to list customer_threads
   
    for c in customer_threads:
        wait() # program waits 
        
        if not queue.full(): # if the queue isnt full
            queue.put(c) # add customer to the queue
            total_customers += 1 # when a customer is added to the queue, 1 is added to the total customers to get how many customers served today
        else:
            rejected_customers += 1 # if the queue is full, 1 will be added to the variable to calculate how many customers had to leave and come back
        c.start()
        c.join() #customer threads are terminated.

    for b in barbers_threads:
        b.join() # the barber threads are terminated.
   
    print("\nChloe's barber shop is now closed.\n") # print statement to say that my barber shop is closed.
    print("Total customer(s) today: ", + total_customers) # prints total number of customers my program served.
    print("Total customer(s) that had to leave and come back: ", + rejected_customers)  #prints total customers that had to leave and come back because my program operates on a list and doesnt end until the whole list has been iterated.


if __name__ == "__main__":
    main()