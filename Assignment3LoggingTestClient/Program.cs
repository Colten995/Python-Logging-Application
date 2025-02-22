/*
 * Filename:    Program.cs
 * Program:     Assignment3LoggingTestClient
 * Programmer:  Luke Alkema
 * Description: This file is the test harness to use the TestClient Class.
 */
using System;
using System.Configuration;

namespace Assignment3LoggingTestClient
{
    //Description: This Program class gets information from the app.config file for the serverIp, port, and delay.
    //Once the parameters have been verified it creates a TestClient object runs the user interface program. 
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



