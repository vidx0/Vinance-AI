# Vinance-AI
An app that utilizes AI to help people take care of their finances with AI integration. Additionally there is an AI that can give stock predictions based on historical trends and sentimental factors. 



predicted file structure

FinanceApp/
│
├── App/
│   ├── AppDelegate.swift    
│   ├── SceneDelegate.swift  
│   ├── Vinance-AIApp.swift  
│
├── Models/
│   ├── User.swift           
│   ├── Transaction.swift    
│   ├── Budget.swift         
│   ├── Investment.swift     
│   ├── PredictionResult.swift     # Data model for storing AI prediction results
│   └── Advice.swift               # Data model for AI-generated financial advice
│
├── Views/
│   ├── Main/
│   │   ├── DashboardView.swift       
│   │   ├── BudgetView.swift          
│   │   ├── TransactionsView.swift    
│   │   ├── InvestmentsView.swift     
│   │   └── SettingsView.swift        
│   │
│   ├── Components/
│   │   ├── TransactionCell.swift     
│   │   ├── ChartView.swift           
│   │   ├── ProgressBar.swift         
│   │   ├── CustomButton.swift        
│   │   └── PredictionCard.swift      # UI component to display AI predictions
│
├── ViewModels/
│   ├── DashboardViewModel.swift      
│   ├── BudgetViewModel.swift         
│   ├── TransactionsViewModel.swift   
│   ├── InvestmentsViewModel.swift    
│   ├── SettingsViewModel.swift       
│   └── AIPredictionViewModel.swift   # Logic for managing AI predictions and recommendations
│
├── AI/
│   ├── AIPredictionService.swift     # Core logic for interacting with the AI model
│   ├── FinancialAnalyzer.swift       # AI logic for analyzing transactions and budgets
│   ├── BudgetOptimizer.swift         # AI logic for creating optimized budgets
│   ├── InvestmentPredictor.swift     # AI logic for generating stock/investment insights
│   └── MLModel/                      # Folder containing CoreML/ONNX model files
│       ├── FinancialModel.mlmodel    # Trained AI model for financial insights
│       └── BudgetAssistant.mlmodel   # Trained AI model for budget optimization
│
├── Services/
│   ├── APIService.swift              
│   ├── PersistenceService.swift      
│   ├── AuthenticationService.swift   
│   ├── NotificationService.swift     
│   ├── AnalyticsService.swift        
│   └── AIModelService.swift          # Manages model loading and inference for AI predictions
│
├── Utils/
│   ├── Constants.swift               
│   ├── Extensions/
│   │   ├── Date+Extensions.swift     
│   │   └── String+Extensions.swift   
│   ├── Validators.swift              
│   ├── Helpers.swift                 
│   └── DataPreprocessor.swift        # Prepares data for AI model input
│
├── Resources/
│   ├── Assets.xcassets               
│   ├── Localizable.strings           
│   ├── Colors.swift                  
│   └── Fonts/                        
│
├── Tests/
│   ├── UnitTests/
│   │   ├── TransactionTests.swift    
│   │   ├── BudgetTests.swift         
│   │   ├── AIPredictionTests.swift   # Tests for AI prediction logic
│   │   └── InvestmentTests.swift     
│   └── UITests/
│       ├── DashboardUITests.swift    
│       └── SettingsUITests.swift     
│
└── README.md                         
