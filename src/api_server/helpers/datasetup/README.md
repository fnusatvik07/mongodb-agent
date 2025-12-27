# 🎓 Hotel Dataset Setup Guide for Candidates

## 📋 Overview
This guide helps you set up a complete **hotel management dataset** in your MongoDB cluster for analytics training. You'll get 3,300+ realistic orders, 450+ customers, and production-grade business data.

## 🚀 Quick Start (5 Minutes)

### Step 1: Download Required Files
Make sure you have these files in your project directory:
```
your-project/
├── datasetup/
│   ├── setup_training_dataset.py    # This setup script
│   └── README.md                    # This guide
├── generate_hotel_data.py           # Data generator
├── import_to_mongodb.py             # MongoDB importer
├── analyze_dataset.py               # Quality verification
└── .env                            # Your configuration (create this)
```

### Step 2: Set Up Environment Variables
Create a `.env` file in your project root with your MongoDB connection:

```bash
# .env file
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

### Step 3: Run Setup Script
```bash
cd your-project
python datasetup/setup_training_dataset.py
```

That's it! The script will automatically:
- Install required packages
- Generate realistic hotel data
- Import to your MongoDB cluster
- Verify data quality (should show 100% score)

## 🔗 MongoDB Setup Options

### Option 1: MongoDB Atlas (Recommended)
**Free tier available - perfect for training**

1. **Sign up**: Go to https://cloud.mongodb.com/
2. **Create cluster**: Choose free tier (M0)
3. **Get connection string**:
   - Click "Connect" → "Connect your application"
   - Copy the connection string
   - Replace `<username>` and `<password>` with your credentials

**Example connection string:**
```
MONGO_URI=mongodb+srv://myusername:mypassword@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

### Option 2: Local MongoDB with Docker
**Quick local setup**

```bash
# Start MongoDB in Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# In your .env file:
MONGO_URI=mongodb://localhost:27017/
```

### Option 3: Local MongoDB Installation
**Install MongoDB directly on your machine**

- **Windows**: Download from https://www.mongodb.com/try/download/community
- **macOS**: `brew install mongodb/brew/mongodb-community`
- **Linux**: Follow https://docs.mongodb.com/manual/administration/install-on-linux/

```bash
# Start MongoDB service
mongod

# In your .env file:
MONGO_URI=mongodb://localhost:27017/
```

## ⚙️ Required Environment Variables

Create a `.env` file in your project root with these variables:

```bash
# REQUIRED: MongoDB Connection
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority

# Optional: Database name (defaults to 'hotel_management')
# DB_NAME=hotel_management

# Optional: Specify collections prefix
# COLLECTION_PREFIX=training_
```

### Environment Variable Details:

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `MONGO_URI` | ✅ **Yes** | MongoDB connection string | `mongodb+srv://user:pass@cluster.net/` |
| `DB_NAME` | No | Database name (default: hotel_management) | `my_training_db` |
| `COLLECTION_PREFIX` | No | Prefix for collection names | `training_` |

## 📦 Prerequisites

### Python Requirements:
- **Python 3.8+** (check with `python --version`)
- **pip** or **uv** package manager

### Required Python Packages:
The setup script will automatically install:
- `pymongo` - MongoDB Python driver
- `python-dotenv` - Environment variable management

### Manual Installation (if needed):
```bash
pip install pymongo python-dotenv
# or with uv:
uv add pymongo python-dotenv
```

## 🔍 Verification Steps

After running the setup script, verify your data:

### Check MongoDB Collections:
```bash
python analyze_dataset.py
```

**Expected output:**
```
🎯 ANALYTICS READINESS SCORE: 100.0%
🎉 EXCELLENT - Ready for production-level analytics!
```

### Verify in MongoDB Compass:
1. Connect to your cluster using MongoDB Compass
2. Check database: `hotel_management`
3. Verify collections:
   - `orders` (3,334 documents)
   - `customers` (450 documents)
   - `delivery_details` (1,778 documents)
   - `menu_items` (33 documents)
   - `users` (8 documents)
   - `audit_logs` (537 documents)

## 🛠️ Troubleshooting

### Common Issues & Solutions:

#### ❌ "Connection refused"
**Problem**: Can't connect to MongoDB
**Solution**:
- Check your `MONGO_URI` in `.env` file
- For Atlas: Verify IP whitelist (add 0.0.0.0/0 for training)
- For local: Ensure MongoDB service is running

#### ❌ "Authentication failed"
**Problem**: Wrong credentials
**Solution**:
- Verify username/password in connection string
- For Atlas: Check database user permissions

#### ❌ "No module named 'pymongo'"
**Problem**: Missing Python packages
**Solution**:
```bash
pip install pymongo python-dotenv
```

#### ❌ "File not found: generate_hotel_data.py"
**Problem**: Missing data generation files
**Solution**:
- Ensure all required files are in your project directory
- Download complete training package

#### ⚠️ "Setup incomplete" or low data counts
**Problem**: Partial data import
**Solution**:
```bash
# Re-run the import
python import_to_mongodb.py
# Or regenerate everything
python datasetup/setup_training_dataset.py
```

### Reset Environment:
If something goes wrong, you can always start fresh:
```bash
# Delete existing data and regenerate
python generate_hotel_data.py
python import_to_mongodb.py
```

## 📊 What You'll Get

After successful setup:

### Database: `hotel_management`
| Collection | Documents | Description |
|------------|-----------|-------------|
| **orders** | 3,334 | Core business transactions with timestamps |
| **customers** | 450 | Customer profiles with segmentation |
| **delivery_details** | 1,778 | Logistics data with performance metrics |
| **menu_items** | 33 | Product catalog with price history |
| **users** | 8 | Staff with role-based permissions |
| **audit_logs** | 537 | Change tracking for compliance |

### Key Metrics:
- **Total Revenue**: ₹28,17,438 over 97 days
- **Average Order Value**: ₹845
- **Customer Segments**: VIP (8%), Regular (35%), Occasional (45%), New (12%)
- **Order Types**: 53.3% delivery, 46.7% dine-in
- **Data Quality**: 100% analytics readiness score

### Business Patterns:
- **Peak Hours**: 12-2 PM (lunch), 7-10 PM (dinner)
- **Weekend Effect**: +40% dine-in orders
- **Seasonal Trends**: Festival season increases, weather impacts
- **Customer Behavior**: Realistic repeat patterns by segment

## 🎯 Next Steps

Once your data is set up:

1. **Explore with MongoDB Compass**: Visual data exploration
2. **Run sample queries**: Try examples in training materials
3. **Start analytics training**: Customer segmentation, revenue analysis
4. **Build aggregation pipelines**: Complex multi-stage queries
5. **Practice GenAI integration**: Natural language to MongoDB queries

## 📚 Additional Resources

- **Dataset Documentation**: See `DATASET_README.md` for technical details
- **Sample Queries**: Check `advanced_analytics_demo.py` for examples
- **MongoDB University**: Free courses at university.mongodb.com
- **Atlas Documentation**: https://docs.atlas.mongodb.com/

## 🆘 Need Help?

1. **Verify setup**: Run `python analyze_dataset.py`
2. **Check logs**: Look for error messages in terminal output
3. **Test connection**: Use MongoDB Compass to connect manually
4. **Ask instructor**: Share error messages and your `.env` configuration (without passwords!)

---

**Ready to start your MongoDB analytics journey?** 🚀

Run `python datasetup/setup_training_dataset.py` and begin exploring production-level hotel business data!