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
            string serverIp = "";
            int serverPort = 0;
            int delay = 0;
            try
            {
                serverIp = ConfigurationManager.AppSettings.Get("ip_address");
                serverPort = Int32.Parse(ConfigurationManager.AppSettings.Get("port"));
                delay = Int32.Parse(ConfigurationManager.AppSettings.Get("delay"));
            }
            catch (Exception ex)
            {
                Console.WriteLine("One or more errors in configuration files. Exiting Program");
                return;
            }

            TestClient client;

            if (string.IsNullOrEmpty(serverIp) || serverPort <= 0 || delay < 0)
            {
                Console.WriteLine("One or more errors in configuation file, using defaults...");
                client = new TestClient();
            }
            else
            {
                client = new TestClient(serverIp, serverPort, delay);
            }
            client.runProgram();
        }
    }
}



