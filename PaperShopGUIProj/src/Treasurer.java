/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */


/**
 *
 * @author DJ
 * Purpose: driver for treasurer program
 */
public class Treasurer {
    private CopyOrder jobs[];
    private double overallIncome;
    private Integer capacity;
    private Integer occupancy;
    
    /**
     * Purpose: to create a treasurer object
     * @param capacityIn 
     */
    
    public Treasurer(Integer capacityIn){
      capacity = capacityIn;
      jobs = new CopyOrder[capacity];
      overallIncome = 0.0;
      occupancy = 0;
    }
    
    /**
     * Purpose: to collect and store information for a job and add it to the list
     * @param color
     * @param paperType
     * @param paperSize
     * @param name
     * @param numberPages
     * @param numberCopies
     * @param binding
     * @return the job number
     */
    
    public Integer addJob(String color, String paperType, String paperSize, String name, Integer numberPages, Integer numberCopies, String binding){
        Integer jobNumber;
        jobNumber = 0;
        
        
        
        while(jobNumber < capacity && jobs[jobNumber] != null){
            jobNumber = jobNumber + 1;
        }
        if(jobNumber != capacity){
            occupancy = occupancy + 1;
            jobs[jobNumber] = new CopyOrder(color, paperType, paperSize, name, numberPages, numberCopies, binding);
        }
        
        return jobNumber;
    }
    
    /**
     * Purpose: to remove a job from the list once the job is complete and keep 
     * track of the total income as jobs are closed
     * @param customerName
     * @return the charges for the customer
     */
    
    public String closeOrder(String customerName){
        double cost;
        Integer jobNumber;
        String charges;
        jobNumber = 0;
        boolean found;
        found = false;
        
        while(jobNumber < capacity && !found){
            
            if(jobs[jobNumber] != null && jobs[jobNumber].getCustomerName().equalsIgnoreCase(customerName)){
                
                found = true;
            }
            else{
                jobNumber = jobNumber + 1;
            }
        }
            
            if(found){
                jobs[jobNumber].determineTotalCost();
                cost = jobs[jobNumber].getTotalCost();
                charges = " Total charges for " + customerName + " are $" + cost;
                jobs[jobNumber] = null;
                occupancy = occupancy - 1;
                overallIncome = overallIncome + cost;
            }
            else{
                charges = customerName + " not found";
            }
            
            
        
        return charges;
    }
    
    /**
     * Purpose to create and show the list of jobs that are added
     * @return the job list
     */
        
        public String[] createJobList(){
            String[] list = new String[occupancy];
            Integer customers = 0;
            double charges;
            for(int ndx = 0; ndx < capacity; ndx++){
                if(jobs[ndx] != null){
                    jobs[ndx].determineTotalCost();
                    charges = jobs[ndx].getTotalCost();
                    list[customers] = jobs[ndx].getCustomerName() + " has job " + ndx + " which costs $" + charges;
                    customers = customers + 1; 
                }
            }
            
            return list;
        }
        
        /**
         * Purpose to allow a customer to change the binding of his current print job
         * @param customerName
         * @return the binding changes
         */
        
        public String changeBinding(String customerName, String newBinding){
            Integer jobNumber;
            String bindingChanges;
            boolean found;
            found = false;
            jobNumber = 0;
            
            while(jobNumber < capacity && !found){
                if(jobs[jobNumber] != null && jobs[jobNumber].getCustomerName().equalsIgnoreCase(customerName)){
                    found = true;
                }
                else{
                    jobNumber = jobNumber + 1;
                }
            }
            
            if(found){
                jobs[jobNumber].setBinding(newBinding);
                bindingChanges = "binding for " + customerName + " is now " + newBinding;
            }
            else{
                bindingChanges = customerName + " not found";
            }
            return bindingChanges;
        }
        
        /**
         * Purpose to get the job capacity
         * @return capacity 
         */
        
        public Integer getCapacity(){
            return capacity;
        }
        
        /**
         * Purpose to get the job occupancy
         * @return occupancy
         */
        
        public Integer getOccupancy(){
            return occupancy;
        }
        
        /**
         * Purpose to get the overall income from the completed jobs
         * @return overall income
         */
        
        public double getOverallIncome(){
            return overallIncome;
        }
                
        
                
    }

