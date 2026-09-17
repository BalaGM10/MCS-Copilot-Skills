## Order-to-Cash Process

```mermaid
sequenceDiagram
    autonumber
    participant Customer
    participant Sales Team
    participant Warehouse
    participant Finance

    Note over Customer: 🟢 Start: Order Received
    Customer->>Sales Team: Submit Order
    
    Sales Team->>Sales Team: Review Order
    
    alt Order Approved? (No)
        Note over Sales Team: 🔴 End: Order Rejected
    else Order Approved? (Yes)
        Note over Sales Team: Split Fulfill & Invoice
        
        par Fulfillment
            Sales Team->>Warehouse: Start Fulfillment
            activate Warehouse
            Warehouse->>Warehouse: Pick and Pack
            Warehouse->>Warehouse: Ship Goods
            deactivate Warehouse
        and Invoicing
            Sales Team->>Finance: Start Invoicing
            activate Finance
            Finance->>Finance: Generate Invoice
            Note right of Finance: 📄 Invoice Document
            Finance->>Finance: Send Invoice
            deactivate Finance
        end
        
        Note over Sales Team: Join Fulfill & Invoice
        Sales Team->>Finance: Process Payment
        activate Finance
        
        loop Retry Payment
            alt Payment Successful? (No)
                Finance->>Finance: Follow up Payment
                Finance->>Finance: Process Payment
            end
        end
        
        Note over Finance: 🔴 End: Order Completed
        deactivate Finance
    end
```

### Mapping Explanations:
- **Pools / Swimlanes**: Represented via sequential `participant` declarations (Customer, Sales Team, Warehouse, Finance).
- **Start / End Events**: Mapped to `Note over [Participant]:` using standard 🟢 Start and 🔴 End emojis.
- **Tasks**: Represented as messages between participants (e.g., `Customer->>Sales Team: Submit Order`) or internal self-referencing messages for tasks completed within a swimlane (e.g., `Warehouse->>Warehouse: Pick and Pack`).
- **Exclusive Gateways**: Converted to `alt` / `else` / `end` conditional blocks (e.g., handling the "Order Approved?" and "Payment Successful?" logic).
- **Parallel Gateways**: Mapped to `par` / `and` / `end` blocks to show the parallel flow between Fulfillment (Warehouse) and Invoicing (Finance).
- **Data Objects**: Modeled as annotations via `Note right of [Participant]: 📄 [Label]`.
- **Activation Markers**: Added to explicitly highlight when specific systems or roles take active responsibility over a sequence.
