using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Net;
using System.Threading.Tasks;
using System.Threading;
using System.Linq.Expressions;
using System.Configuration;
using System.Collections.Specialized;
using System.Runtime.Remoting.Messaging;

namespace Assignment3LoggingTestClient
{

    public class TestClient
    {
        private string serverIp = "";
        private int serverPort = 0;
        private int delay = 0;
        private UdpClient udpClient;

        public TestClient() : this("127.0.0.1", 13000, 500)
        {
        }

        public TestClient(string newServerIp, int newServerPort, int newDelay)
        {
            serverPort = newServerPort;
            serverIp = newServerIp;
            udpClient = new UdpClient();
            udpClient.Connect(serverIp, serverPort);
            delay = newDelay;
        }

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
        public void manualTest()
        {
            Console.WriteLine("Please Enter Log Message to Send >>");
            string message = Console.ReadLine();
            sendLog(message);
        }
        public void printMenu()
        {
            Console.WriteLine("-----------Menu-----------");
            Console.WriteLine("  1. Run Automated Tests");
            Console.WriteLine("  2. Run Manual Test");
            Console.WriteLine("  3. Quit");
            Console.WriteLine("--------------------------");
        }

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