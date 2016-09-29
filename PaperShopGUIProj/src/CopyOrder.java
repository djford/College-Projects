/*
 * Purpose:  determine the cost of a print order
 * Author:  Sharon Stansfield
 * Modified:  3/19/13
 */


/**
 *Purpose:  Objects of this class represent one copy order
 * @author Sharon
 */
public class CopyOrder {
    //properties
    private Page copy;  //handles cost per page
    private String customerName;
    private int numberCopies;
    private int numberPages;
    private String binding;
    private double totalCost;
    private String orderDetails;  //a string representing the details of the order
    
    /**
     * Purpose:  parameterized constructor
     * @param customerNameIn
     * @param colorIn
     * @param paperTypeIn
     * @param paperSizeIn
     * @param copiesIn
     * @param pagesIn
     * @param bindingIn 
     */
    public CopyOrder(String colorIn, String paperTypeIn, String paperSizeIn,
             String customerNameIn, int pagesIn, int copiesIn, String bindingIn){
        copy = new Page(colorIn, paperTypeIn, paperSizeIn);
        customerName=customerNameIn;
        numberCopies = copiesIn;
        numberPages = pagesIn;
        binding=bindingIn;
        totalCost=0.0;
        orderDetails="";
       
    }
    
    /**
     * Purpose:  determine the total cost of the copy job
     */
    public void determineTotalCost(){
        double costPerPage;
        //determine the cost per page using the copy object
        totalCost = 0.0;
        copy.determinePricePerPage();
        costPerPage = copy.getCostPerPage();
        
        //total cost of copies
        totalCost = costPerPage * numberPages * numberCopies;
        
        //additional cost of binding if desired
        if (binding.equalsIgnoreCase("glue")){
            totalCost = totalCost + 25.00 * numberCopies;
        }
        else if (binding.equalsIgnoreCase("spiral")){
            totalCost = totalCost + 10.00 * numberCopies;   
        }
        // if "none" than the cost doesn't change
    }
    
    /**
     * Purpose create a string that shows the details of the order
     */
    public void createOrderDetail(){
        orderDetails = "Total costs for " + customerName +"'s order are $" +
                totalCost;
    }
    
    /**
     * Purpose:  accessor for customer name
     * @return customer name (string)
     */
    public String getCustomerName(){
        return customerName;
    }
    
    /**
     * accessor for order details
     * @return order details (string)
     */
    public String getOrderDetails(){
        return orderDetails;
    }
    
    /**
     * accessor for numberOfCopies
     * @return numberOfCopies (int)
     */
    public int getNumberCopies(){
        return numberCopies;
    }
    
    /**
     * Purpose: accessor for numberOfPages
     * @return numberOfPages (int)
     */
     public int getNumberPages(){
        return numberPages;
    }
     
     /**
      * Purpose:  accessor for totalCost
      * @return totalCost (double)
      */
    public double getTotalCost(){
        return totalCost;
    }
    
    /**
      * Purpose:  accessor binding
      * @return totalCost (double)
      */
    public String getBinding(){
        return binding;
    }
    
    /**
     * Purpose:  mutator for binding
     * @param bindingIn type of binding (spiral, glue, none)
     */
    public void setBinding(String bindingIn){
        binding=bindingIn;
    }
}
