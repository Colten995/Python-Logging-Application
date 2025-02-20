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


namespace Assignment3LoggingTestClient
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string serverIp = ConfigurationManager.AppSettings.Get("ip_address");
            int serverPort = Int32.Parse(ConfigurationManager.AppSettings.Get("port"));
            int delay = Int32.Parse(ConfigurationManager.AppSettings.Get("delay"));
            try
            {
                using (UdpClient udpClient = new UdpClient())
                {
                    udpClient.Connect(serverIp, serverPort);

                    string[] messages = {
                    "1|INFO|Application started.",
                    "1|DEBUG|Initializing components.",
                    "3|WARN|Low memory warning!",
                    "Malformed line",
                    "4|ERROR|Divide by zero occurred!",
                    "5|FATAL|Unexpected crash detected." };

                    foreach (string message in messages)
                    {
                        byte[] data = Encoding.UTF8.GetBytes(message);
                        udpClient.Send(data, data.Length);
                        Console.WriteLine($"Sent: {message}");

                        Thread.Sleep(delay); 
                    }

                    Console.WriteLine("Finished sending messages.");
                }
            }
            catch (SocketException ex)
            {
                Console.WriteLine($"[ERROR] Failed to send data: {ex.Message}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[ERROR] Unexpected error: {ex.Message}");
            }
        }
    }
}



