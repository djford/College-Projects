


/**
 *
 * @author sstansfield
 */
public class Page {
    //properties:
    private String color;
    private String paperType;
    private String paperSize;
    private double costPerPage;
    
    public Page(String colorIn, String paperTypeIn, String paperSizeIn){
        color = colorIn;
        paperType = paperTypeIn;
        paperSize = paperSizeIn;
        costPerPage = 0.0;
    }//Page constructor
    
    public void determinePricePerPage(){
       
        //cost for color
        costPerPage = 0.0;
        if (color.equalsIgnoreCase("Full")){
            costPerPage = costPerPage + 0.10;
        }
        else if (color.equalsIgnoreCase("P1")) {
            costPerPage = costPerPage + 0.30;
        }
        else if (color.equalsIgnoreCase("P2")) {
            costPerPage = costPerPage + 0.45;
        }
        else if (color.equalsIgnoreCase("P3")) {
            costPerPage = costPerPage + 0.65;
        }
    
       // cost for paper type
        if (paperType.equalsIgnoreCase("Matte")) {
            costPerPage = costPerPage + 0.20;
        }
        else if (paperType.equalsIgnoreCase("Glossy")) {
            costPerPage = costPerPage + 0.30;
        }
        else if (paperType.equalsIgnoreCase("Luster")) {
            costPerPage = costPerPage + 0.60;
        }
    
        //cost for paper size
        if(paperSize.equalsIgnoreCase("A4")){
            costPerPage = costPerPage*1.75;
        }
    }
    
    public double getCostPerPage(){
        return costPerPage;
    }
}
