import java.io.File;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import java.lang.Integer;
//import java.util.Scanner;

public class XMLGenerator {

    public static void main(String argv[]) throws Exception {
        DocumentBuilderFactory docFactory = DocumentBuilderFactory.newInstance();
        DocumentBuilder docBuilder = docFactory.newDocumentBuilder();

        Document doc = docBuilder.newDocument();
        Element rootElement = doc.createElement("a");
        doc.appendChild(rootElement);
        //Scanner sc = new Scanner(System.in);
        //int N = sc.nextInt();
        int N = Integer.parseInt(argv[0]);
        //int N = 100;
        HashMap<String, String> m = new HashMap<>();
        m.put("a", "((bc)*d)*");
        m.put("b", "a*");
        m.put("c", "d*");
        m.put("d", "_");

        int nb = 1;
        Queue<Element> q = new LinkedList<>();
        q.add(rootElement);
        while (nb < N) {
            int k = (int) Math.floor(Math.random()*1000);
            if (q.isEmpty()) {
                q.add(rootElement);
                continue;
            }

            //System.out.println("K is "+k);

            Element s = q.poll();

            String gen = new String("");

            if (s.getNodeName().equals("a")) {
                //System.out.println("I am in a");
                for (int i=0;i<k;i++) {
                    gen = gen + "bc";
                    nb += 2;
                }
                gen = gen + "d";
                nb += 1;
                if (gen.matches(m.get("a"))) {
                    for (int i=0;i<gen.length();i++) {
                        Element el = doc.createElement(""+gen.charAt(i));
                        el.appendChild(doc.createTextNode(" "));
                        s.appendChild(el);
                        q.add(el);
                    }
                } else {
                    nb -= 2*k - 1;
                    System.out.println("Problem : m.get(\"a\")="+m.get("a")+" and gen="+gen);
                }
            }

            if (s.getNodeName().equals("b")) {
                //System.out.println("I am in b");
                for (int i=0;i<k;i++) {
                    gen += "a";
                    nb += 1;
                }

                if (gen.matches(m.get("b"))) {
                    for (int i=0;i<gen.length();i++) {
                        Element el = doc.createElement(""+gen.charAt(i));
                        el.appendChild(doc.createTextNode(" "));
                        s.appendChild(el);
                        q.add(el);
                    }
                } else {
                    nb -= k;
                    System.out.println("Problem : m.get(\"b\")="+m.get("b")+" and gen="+gen);
                }
            }

            if (s.getNodeName().equals("c")) {
                //System.out.println("I am in c");
                for (int i=0;i<k;i++) {
                    gen += "d";
                    nb += 1;
                }

                if (gen.matches(m.get("c"))) {
                    for (int i=0;i<gen.length();i++) {
                        Element el = doc.createElement(""+gen.charAt(i));
                        el.appendChild(doc.createTextNode(" "));
                        s.appendChild(el);
                        q.add(el);
                    }
                } else {
                    nb -= k;
                    System.out.println("Problem : m.get(\"c\")="+m.get("c")+" and gen="+gen);
                }
            }

            if (s.getNodeName().equals("d")) {
                continue;
            }
        }

        TransformerFactory transformerFactory = TransformerFactory.newInstance();
        Transformer transformer = transformerFactory.newTransformer();
        DOMSource source = new DOMSource(doc);
        StreamResult result = new StreamResult(new File("test"+N+".xml"));
        transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
        transformer.transform(source, result);
        System.out.println("File saved!");
    }
}
