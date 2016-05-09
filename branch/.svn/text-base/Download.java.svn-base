/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

//package scheduler;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

/**
 *
 * @author gonga
 */
public class Download extends Thread{
    private Process downloadProcess;
    public static final String SERIALDUMP_LINUX = "/home/gonga/contiki-2.x/tools/sky/serialdump-linux";

    public DataInputStream dis   = null;
    public DataOutputStream dos  = null;

    private static  int mote_id = 1;

    public Download(int id){
        mote_id = id;
  
        this.start();
    }

    public void run(){

         String cmd ="make login MOTE="+mote_id;
         try{
              System.out.println("==> recvCmd: " + cmd);

              downloadProcess= Runtime.getRuntime().exec(cmd);

            final BufferedReader input = new BufferedReader(new InputStreamReader(downloadProcess.getInputStream()));
            final BufferedReader err = new BufferedReader(new InputStreamReader(downloadProcess.getErrorStream()));
            
            Thread readThread = new Thread(new Runnable() {

                 public void run() {
                     String response = "";
                   
                     try {
             
                         while ((response = input.readLine()) != null) {
                             System.out.println(response);
                             
                         }
                                               
                         input.close();
                         downloadProcess.destroy();
                     } catch (Exception ex) {                        
                         ex.printStackTrace();
                         downloadProcess.destroy();
                     }
                 }
             });  //end of T1

             Thread readErr = new Thread(new Runnable() {

                 public void run() {
                     String response = "";
                     try {
                         while ((response = err.readLine()) != null) {
                             System.out.println(response);
                         }

                         err.close();                      
                     } catch (Exception ex) {
                         ex.printStackTrace();
                     }
                 }
             });

             readThread.start();
             readErr.start();

         }catch(Exception ex){
            downloadProcess.destroy();
            ex.printStackTrace();
         }
    }
 

  
    public static void main(String[] args) {
        // TODO code application logic here
        int mote_id = 14;
        try {
            mote_id = Integer.parseInt(args[0]);
            
            System.out.println("mote_id: "+mote_id);
            
            Download d = new Download(mote_id);
        } catch (Exception ex) {
            System.out.println("error: execute like: java Download <moteid>");
            System.out.println("expecific example: java Download 1\n this will connect to /dev/ttyUSB0");
        }
    }
}

/*
     public void downloadFiles() {

        isDownloadingFiles = true;

        String cmd = "./download " + (gateway.motelist.size() - 1) + " \n";

        System.out.println("==> recvCmd: " + cmd);

        try {
            serverIf.notifyNewMessage("==> recvCmd: " + cmd);

            downloadProcess= Runtime.getRuntime().exec(cmd);

            final BufferedReader input = new BufferedReader(new InputStreamReader(downloadProcess.getInputStream()));
            final BufferedReader err = new BufferedReader(new InputStreamReader(downloadProcess.getErrorStream()));

            Thread readInput = new Thread(new Runnable() {

                public void run() {
                    String response = "";
                    try {

                        while ((response = input.readLine()) != null) {
                            //System.out.println(response);
                            //serverIf.notifyNewMessage("==> download: " + response);
                            if(response.contains(".txt") || response.contains("sensor flushed.")){
                                //System.out.println(response);
                                serverIf.notifyNewMessage("==> download: " + response);
                            }
                        }

                        input.close();

                        serverIf.notifyNewMessage("==>cient download files from Motes/finished....");

                        //System.out.println("==>download thread done...");

                        synchronized(this){
                                isDownloadingFiles = false;
                        }

                        downloadProcess.destroy();
                        downloadProcess = null;
                    } catch (Exception ex) {
                        ex.printStackTrace();
                    }

                    System.out.println("calling upload files to server....");
                    uploadFilestoServer();
                }
            });

            Thread readErr = new Thread(new Runnable() {

                public void run() {
                    String response="";
                    try {

                        //System.out.println("==>possible erros here...");
                        while ((response = err.readLine()) != null) {
                            System.out.println(response);
                        }

                        err.close();

                        serverIf.notifyNewMessage("==>download files errors here....");

                        isDownloadingFiles = false;
                        //System.out.println("==>error thread done...");
                    } catch (Exception ex) {
                        ex.printStackTrace();
                    }
                }
            });

            readInput.start();
            readErr.start();

        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
 */
/*
  public void uploadFilestoServer() {
        isUploadingFiles = true;
        try {
            UploadResults upload = new UploadResults();
            upload.start();
            serverIf.notifyNewMessage("==>download thread started......");
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
 */

/*
  class UploadResults extends Thread{

        public UploadResults(){

        }
        public void run() {
            try {
                isUploadingFiles = true;
                serverIf.notifyNewMessage("==>upload thread called run......");
                try {
                    BufferedInputStream bis = null;

                    File folder = new File("./");
                    File[] listOfFiles = folder.listFiles();

                    //System.out.println("==>uploading files to the server..");

                    for (int i = 0; i < listOfFiles.length; i++) {
                        if (listOfFiles[i].isFile()) {
                            String filename = "./" + listOfFiles[i].getName().trim();

                            //serverIf.notifyNewMessage("==>filename: "+filename);

                            if (filename.contains("link") && filename.endsWith(".txt")) {
                                if (listOfFiles[i].canRead()) {
                                    //int fileSize = listOfFiles[i].s
                                    File file = new File(filename);
                                    bis = new BufferedInputStream(new FileInputStream(file));
                                    int fileSize = (int) file.length();
                                    byte[] data = new byte[fileSize];

                                    //ResultFile res = new ResultFile(filename, fileSize);
                                    //bis.read(res.fileData, 0, res.fileSize);

                                    bis.read(data, 0, data.length);

                                    //System.out.println("==>uploading file:" + filename);
                                    serverIf.notifyFileAvailable(filename, data);

                                    bis.close();

                                    if (file.delete()) {
                                        //System.out.println("file deleted..");
                                    }
                                }
                            }
                        }
                    }

                    isUploadingFiles = false;

                } catch (Exception ex) {
                    ex.printStackTrace();
                }
                //System.out.println("==>uploading files to the server finished");

            } catch (Exception ex) {
                ex.printStackTrace();
            }

            isUploadingFiles = false;
        }
    }
 */