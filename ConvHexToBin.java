
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.ArrayList;

public class ConvHexToBin extends Thread {

    private static int MASK [] = {0x8000, 0x4000, 0x2000, 0x1000,
                                  0x0800, 0x0400, 0x0200, 0x0100,
                                  0x0080, 0x0040, 0x0020, 0x0010,
                                  0x0008, 0x0004, 0x0002, 0x0001};

    private final String[] res ={"0000", "0001", "0010", "0011",
                             "0100", "0101", "0110", "0111",
                             "1000", "1001", "1010", "1011",
                             "1100", "1101", "1110", "1111"};

    private static final String[] reschar ={"0", "1", "2", "3",
                                     "4", "5", "6", "7",
                                     "8", "9", "10", "11",
                                     "12", "13", "14", "15"};
    
    public ConvHexToBin() {
    }

    public void run() {
        try {

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
                            BufferedInputStream input = new BufferedInputStream(new FileInputStream(file));

                            String newFileName = "./".concat(file.getName().replaceAll(".txt", ".res").replaceAll("./", ""));
                            BufferedOutputStream bos = new BufferedOutputStream(new FileOutputStream(newFileName));
                            int nbytes = (int)file.length();
                            byte[] buff = new byte[nbytes];

                            input.read(buff, 0, buff.length);

                            ArrayList<String> strList = new ArrayList<String>();
                            String charBuf="";
                            for(int n = 0; n < buff.length; n++){
                                charBuf += (char)buff[n];                          
                            }

                            String[] newStr = charBuf.split("\n");

                            for (int n = 0; n < newStr.length; n++) {
                                String bits = newStr[n].split("-")[1];
                                //System.out.print(bits+"-");
                                for (int k = 0; k < bits.length(); k++) {
                                    //if (bits.charAt(k) != '"') {
                                        int num = Integer.parseInt("" + bits.charAt(k), 16);
                                        //System.out.print(res[num]);
                                        for(int l = 0; l < res[num].length(); l++){
                                            bos.write((byte)res[num].charAt(l));
                                        }
                                    //}                                    
                                }
                                bos.write((char)'\n');
                                bos.flush();
                                //System.out.println();
                            }
                            bos.close();
                            input.close();
                        }
                        System.out.println();
                    }
                }
            }

        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public static void main(String[] args) {
        // TODO code application logic here
        int mote_id = 14;

         ConvHexToBin ch2b = new ConvHexToBin();
         ch2b.start();
    }
}
