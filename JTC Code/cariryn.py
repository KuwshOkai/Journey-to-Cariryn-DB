from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

cariryndb = mysql.connector.connect(user = "root", password = "Yggdras1lDelt@",
                                    host = '127.0.0.1', database = "cariryn")
                                    #auth_plugin = 'my_sql_native_password'

@app.route('/', methods=['GET', 'POST'])
def index():
    if "character" in request.form:
        return render_template('/addchar.html', data1 = getrace(), data2 = getclass(), data3 = getalignment(), data4 = getarmour())
    elif "inventory" in request.form:
        return render_template('/inventory.html')
    elif "items" in request.form:
        return render_template('/items.html')
    elif "npc" in request.form:
        return render_template('/npcs.html')
    elif "encounter" in request.form:
        return render_template('/encounter.html')
    elif "location" in request.form:
        return render_template('/addlocation.html')
    else:
        return render_template('/index.html')


@app.route('/encounter',methods=['GET','POST'])
def encounter():
    if "addencounter" in request.form:
        return render_template('/newencounter.html', data1 = getlocation(), data2 = getnpc(), data3 = getenemy(), data4 = getitem())
    elif "allencounters" in request.form:
        return render_template('/allencounters.html', data1 = viewallencounters(), data2 = getenemy())
    elif "viewencounter" in request.form:
        return render_template('/specificencounter.html', data1 = viewallencounters(), data2 = getenemy())
    else:
        return render_template('/index.html')



@app.route('/inventory', methods=['GET','POST'])
def inventory():
    if "allitems" in request.form:
        return render_template('/viewinventory.html',data=getplayer())
    elif "changeinv" in request.form:
        return render_template('/modifyinventory.html',data=getplayer())
    else:
        return render_template('/inventory.html')


@app.route('/viewinventory', methods=['GET', 'POST'])
def viewinventory():
  #Takes details from form and crafts a sql statement         
  if "submit" in request.form:
      details = request.form
      PlayerID = getplayerid(details['Player'])
      Int_PlayerID = PlayerID[0]
      Int_PlayerID = str(Int_PlayerID[0])  
      return render_template('/modifyinventory.html',data =getinventory(Int_PlayerID), data2 = getsum(Int_PlayerID), data3 = Int_PlayerID,data4=getplayer(), data5 = getitem())      
  elif "cancel" in request.form:
        pass
  return render_template('/index.html')


@app.route('/modifyinventory', methods=['GET', 'POST'])
def modifyinventory():
  #Takes details from form and crafts a sql statement         
  if "submit" in request.form:
      details = request.form
      InventoryID = details['Remove']
      cur = cariryndb.cursor()
      sql = "DELETE FROM inventory where inventory.InventoryID = %s"
      nq = InventoryID
      cur.execute(sql,(nq,))
      cariryndb.commit()
      cur.close()   
      return render_template('/viewinventory.html',data=getplayer()) 
  if "add" in request.form:
      details = request.form 
      PlayerID = getplayerid(details['Player']) 
      Int_PlayerID = PlayerID[0]
      Int_PlayerID = int(Int_PlayerID[0])  
      ItemID = getitemid(details['Item']) 
      Int_ItemID = ItemID[0]
      Int_ItemID = int(Int_ItemID[0])
      cur = cariryndb.cursor()
      cur.execute("INSERT INTO inventory(PlayerID, ItemID) VALUES (%s, %s)", (Int_PlayerID, Int_ItemID))
      cariryndb.commit()
      cur.close()      
  elif "cancel" in request.form:
        pass
  return render_template('/index.html')

@app.route('/items', methods=['GET','POST'])
def items():
    if "additem" in request.form:
        return render_template('/additem.html', data = getitemtype())
    elif "viewitems" in request.form:
        return render_template('/viewitems.html', data=viewitems())
    else:
        return render_template('/index.html')


@app.route('/specificencounter', methods=['GET', 'POST'])
def viewsortedencounter():
  #Takes details from form and crafts a sql statement         
  if "submit" in request.form:
      details = request.form
      Enemy = details['enemy']
      return render_template('/specificencounter.html',data1 = viewsortencounters(Enemy), data2 = getenemy())      
  elif "cancel" in request.form:
        pass
  return render_template('/index.html')

@app.route('/additem', methods=['GET','POST'])
def additem():
    if "submit" in request.form:
        details = request.form
        Name = details['Name']
        Cost = details['cost']
        Load = details['load']
        ItemTypeID = getitemtypeid(details['ItemType'])
        Int_ItemTypeID = ItemTypeID[0]
        Int_ItemTypeID = int(Int_ItemTypeID[0])  
        cur = cariryndb.cursor()
        cur.execute("INSERT INTO items(Name, Cost, `Load`, ItemTypeID) VALUES (%s, %s, %s, %s)", (Name, Cost, Load, Int_ItemTypeID))
        cariryndb.commit()
        cur.close()        
    elif "cancel" in request.form:
            pass
    return render_template('/index.html')

@app.route('/addchar', methods=['GET', 'POST'])
def addchar():

  #Takes details from form and crafts a sql statement  
  if "submit" in request.form:
          details = request.form
          FirstName = details['FirstName']
          LastName = details['LastName']    
          RaceID = getraceid(details['Race'])
          ClassID = getclassid(details['Class'])
          AlignmentID = getalignmentid(details['Alignment'])
          Int_RaceID = RaceID[0]
          Int_RaceID = int(Int_RaceID[0])
          Int_ClassID = ClassID[0]
          Int_ClassID = int(Int_ClassID[0])
          Int_AlignmentID = AlignmentID[0]
          Int_AlignmentID = int(Int_AlignmentID[0])

          Level = details['level']
          Strength = details['strength']
          Brawn = details['brawn']
          Agility = details['agility']
          Mettle = details['mettle']
          Craft = details['craft']
          Insight = details['insight']

          Wits = details['wits']
          Resolve = details['resolve']
          Life = details['life']

          ArmourID = getarmourid(details['Armour'])
          Int_ArmourID = ArmourID[0]
          Int_ArmourID = int(Int_ArmourID[0])

          Shield = details['Shield']
          Helm = details['Helm']

          cur = cariryndb.cursor()
          cur.execute("INSERT INTO pcs(FirstName, LastName, RaceID, ClassID, AlignmentID,Level,Strength,Brawn,Agility,Mettle,Craft,Insight,Wits,Resolve,Life,Shield,Helm, ArmourID) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (FirstName, LastName, Int_RaceID,Int_ClassID, Int_AlignmentID,Level,Strength,Brawn,Agility,Mettle,Craft,Insight,Wits,Resolve,Life,Shield,Helm,Int_ArmourID))
          cariryndb.commit()
          cur.close()
          
  elif "cancel" in request.form:
        pass
  return render_template('/index.html')

@app.route('/npcs', methods=['GET','POST'])
def npcs():
    if "addnpc" in request.form:
        return render_template('/addnpc.html')
    elif "viewnpc" in request.form:
        return render_template('/viewnpcs.html', data=viewnpcs())
    else:
        return render_template('/index.html')




@app.route('/addnpc', methods=['GET', 'POST'])
def addnpc():    
    if "submit" in request.form:
        details = request.form
        Name = details['Name']
        Strength = details['strength']
        Craft = details['craft']
        Life = details['life']
        cur = cariryndb.cursor()
        cur.execute("INSERT INTO npcs(Name, Strength, Craft, Life) VALUES (%s, %s,%s,%s)", (Name, Strength, Craft, Life))
        cariryndb.commit()
        cur.close()        
    elif "cancel" in request.form:
        pass
    return render_template('/index.html')

@app.route('/addlocation',methods=['GET','POST'])
def addlocation():
    if "submit" in request.form:
        details = request.form
        Name = details['Name']
        Description = details['Description']
        cur = cariryndb.cursor()
        cur.execute("INSERT INTO locations(Name, Description) VALUES (%s, %s)", (Name, Description))
        cariryndb.commit()
        cur.close()        
    elif "cancel" in request.form:
            pass
    return render_template('/index.html')



@app.route('/newencounter',methods=['GET','POST'])
def newencounter():
    if "add" in request.form:
        details = request.form 
        LocationID = getlocationid(details['location']) 
        Int_LocationID = LocationID[0]
        Int_LocationID = int(Int_LocationID[0]) 
        NPCID = getnpcid(details['npc']) 
        Int_NPCID = NPCID[0]
        Int_NPCID = int(Int_NPCID[0])  
        EnemyID = getenemyid(details['enemy']) 
        Int_EnemyID = EnemyID[0]
        Int_EnemyID = int(Int_EnemyID[0])   
        ItemID = getitemid(details['item']) 
        Int_ItemID = ItemID[0]
        Int_ItemID = int(Int_ItemID[0])
        cur = cariryndb.cursor()
        cur.execute("INSERT INTO encounters(LocationID, NPCID, EnemyID, ItemID) VALUES (%s, %s, %s, %s )", (Int_LocationID, Int_NPCID,Int_EnemyID, Int_ItemID))
        cariryndb.commit()
        cur.close()      
    elif "cancel" in request.form:
            pass
    return render_template('/index.html')




def getrace():
    cur = cariryndb.cursor()
    cur.execute("Select Name FROM races")
    data = cur.fetchall()   
    return data

def getraceid(name):
    cur = cariryndb.cursor()
    query = ("Select RaceID FROM races where Name='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getclass():
    cur = cariryndb.cursor()
    cur.execute("Select ClassName FROM classes")
    data = cur.fetchall()
    return data

def getclassid(name):
    cur = cariryndb.cursor()
    query = ("Select ClassID FROM classes where ClassName='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getalignment():
    cur = cariryndb.cursor()
    cur.execute("Select AlignmentType FROM alignment")
    data = cur.fetchall()
    return data

def getalignmentid(name):
    cur = cariryndb.cursor()
    query = ("Select AlignmentID FROM alignment where AlignmentType='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getarmourid(name):
    cur = cariryndb.cursor()
    query = ("Select ArmourID FROM armour where Name='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getarmour():    
    cur = cariryndb.cursor()
    cur.execute("Select Name FROM armour")
    data = cur.fetchall()
    return data

def getitemtype():
    cur = cariryndb.cursor()
    cur.execute("Select Name FROM itemtypes")
    data = cur.fetchall()
    return data

def getitemtypeid(name):
    cur = cariryndb.cursor()
    query = ("Select ItemTypeID FROM itemtypes where Name='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getlocationid(name):
    cur = cariryndb.cursor()
    query = ("Select LocationID FROM locations where Name='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getnpcid(name):
    cur = cariryndb.cursor()
    query = ("Select npcID FROM npcs where Name='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getenemyid(name):
    cur = cariryndb.cursor()
    query = ("Select EnemyID FROM enemies where Name='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getitemid(name):
    cur = cariryndb.cursor()
    query = ("Select ItemID FROM items where Name='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getlocation():
    cur = cariryndb.cursor()
    cur.execute("Select Name FROM locations")
    data = cur.fetchall()
    return data

def getnpc():
    cur = cariryndb.cursor()
    cur.execute("Select Name FROM npcs")
    data = cur.fetchall()
    return data

def getenemy():
    cur = cariryndb.cursor()
    cur.execute("Select Name FROM enemies")
    data = cur.fetchall()
    return data

def getitem():
    cur = cariryndb.cursor()
    cur.execute("Select Name FROM items")
    data = cur.fetchall()
    return data

def viewnpcs():
    cur = cariryndb.cursor()
    cur.execute("SELECT Name, Strength, Craft, Life FROM npcs")
    data = cur.fetchall()
    return data

def viewitems():
    cur = cariryndb.cursor()
    cur.execute("SELECT items.Name, Cost, items.Load, itemtypes.Name FROM items, itemtypes where items.ItemtypeID = itemtypes.ItemTypeID ORDER by Cost Desc;")
    data = cur.fetchall()
    return data

def viewallencounters():
    cur = cariryndb.cursor()
    cur.execute("SELECT EncounterID, locations.Name, npcs.Name, enemies.Name, items.Name FROM locations, npcs,enemies,items,encounters where locations.LocationID = encounters.LocationID and npcs.NPCID = encounters.NPCID and enemies.EnemyID = encounters.EnemyID and items.ItemID = encounters.ItemID;")
    data = cur.fetchall()
    return data

def viewsortencounters(name):
    cur = cariryndb.cursor()
    cur.execute("SELECT EncounterID, locations.Name, npcs.Name, enemies.Name, items.Name FROM locations, npcs,enemies,items,encounters where encounters.EnemyID = enemies.EnemyID and locations.LocationID = encounters.LocationID and npcs.NPCID = encounters.NPCID and enemies.EnemyID = encounters.EnemyID and items.ItemID = encounters.ItemID and enemies.Name = '"+name+"'")
    data = cur.fetchall()
    return data


def getinventory(name):
    cur = cariryndb.cursor()
    query=("SELECT InventoryID, items.Name, Cost, items.Load, itemtypes.Name FROM cariryn.inventory, items, itemtypes where PlayerID = '"+name+"' and inventory.ItemID = items.ItemID and items.ItemtypeID = itemtypes.ItemTypeID")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getplayerid(name):
    cur = cariryndb.cursor()
    query = ("Select PlayerID FROM pcs where `FirstName`='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

def getplayer():
    cur = cariryndb.cursor()
    cur.execute("Select `FirstName` FROM pcs")
    data = cur.fetchall()
    return data

def getsum(name):
    cur = cariryndb.cursor()
    query=("Select sum(`Load`) from cariryn.inventory, items, itemtypes where PlayerID = '"+name+"' and inventory.ItemID = items.ItemID     and     items.ItemtypeID = itemtypes.ItemTypeID")
    cur.execute(query)
    data = cur.fetchall()
    return data

if __name__ == '__main__':
    app.run(debug=True)
