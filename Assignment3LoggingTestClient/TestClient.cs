/*
 * Filename:    TestClient.cs
 * Program:     Assignment3LoggingTestClient
 * Programmer:  Luke Alkema
 * Description: This file holds the TestClient class for the project. * 
 */
using System;
using System.ComponentModel;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace Assignment3LoggingTestClient
{

    /*
     * Class:       TestClient
     * Description: This class has the functionality to send log messages to a UDP server on the IP address and port specified. 
     *              The class has a automated test to run preset log messages to the server, as well as the ablity to send manual ones.
     */
    public class TestClient
    {
        private string serverIp = "";
        private int serverPort = 0;
        private int delay = 0;
        private UdpClient udpClient;

        //Default Constructor calls other constructor with parameters
        public TestClient() : this("127.0.0.1", 13000, 500)
        {
        }

        //Overloaded Constructor, takes Ip address, port, and delay for automated tests
        public TestClient(string newServerIp, int newServerPort, int newDelay)
        {
            serverPort = newServerPort;
            serverIp = newServerIp;
            udpClient = new UdpClient();
            udpClient.Connect(serverIp, serverPort);
            delay = newDelay;
        }

        //Parameters: String - logMessage
        //Returns:    void
        //Description: sends a string message via UDP connection to server class is connected to
        public void sendLog(string logMessage)
        {
            try
            {
                byte[] data = Encoding.UTF8.GetBytes(logMessage);
                udpClient.Send(data, data.Length);
                Console.WriteLine($"Sent Log Message: {logMessage}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error sending log: {ex.Message}");
            }
        }

        //Parameters: void
        //Returns:    void
        //Description: sends logs in a loop and delay's between each.
        public void automatedTest()
        {
            string[] messages = {
                    "1|LUKE|Application started.",
                    "1|DEBUG|Initializing components.",
                    "3|WARN|Low memory warning!",
                    "Malformed line",
                    "4|ERROR|Divide by zero occurred!",
                    "5|FATAL|Unexpected crash detected." };

            //Testing 5 different log messages
            foreach (string message in messages)
            {
                sendLog(message);
                Thread.Sleep(delay);
            }

            //Test over-logging by sending 125 random logs
            Random messageNum = new Random();
            for (int i = 0; i < 125; i++)
            {
                sendLog(messages[messageNum.Next(messages.Length)]);
            }
        }


        //Parameters: void
        //Returns:    void
        //Description: Allows user to enter a string to log manually
        public void manualTest()
        {
            Console.WriteLine("Please Enter Log Message to Send >>");
            string message = Console.ReadLine();
            sendLog(message);
        }


        //Parameters: void
        //Returns:    void
        //Description: prints a menu
        public void printMenu()
        {
            Console.WriteLine("-----------Menu-----------");
            Console.WriteLine("  1. Run Automated Tests");
            Console.WriteLine("  2. Run Manual Test");
            Console.WriteLine("  3. Quit");
            Console.WriteLine("--------------------------");
        }


        //Parameters: void
        //Returns:    void
        //Description: Runs a user interface to use the class in a user friendly manner.
        public void runProgram()
        {
            while (true)
            {
                Console.Clear();
                printMenu();
                ConsoleKeyInfo choice = Console.ReadKey(true);
                if (choice.Key == ConsoleKey.D1)
                {
                    automatedTest();
                }
                else if (choice.Key == ConsoleKey.D2)
                {
                    manualTest();
                }
                else if (choice.Key == ConsoleKey.D3)
                {
                    break;
                }
                else
                {
                    Console.WriteLine($"Incorrect Choice. Please Choose Valid Option");
                }

                Console.WriteLine("\n\nPress any key to continue...");
                Console.ReadKey(true);
            }
        }
    }
}