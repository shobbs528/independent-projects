<?php

function OpenConnection()
{
  $host="";
  $cnxnOptions = array("Database"=>"", "Uid"=>"","PWD"=>"");

  $connection = sqlsrv_connect($host, $cnxnOptions);

  if($connection == false)
      die(FormatErrors(sqlsrv_errors()));

  return $connection;
}


function getCarRentalData(){
  $carRentalData = array();
  $carRentalData[1] = $_POST['vin'];
  $carRentalData[2] = $_POST['custID'];
  $carRentalData[3] = $_POST['transNum'];
  $carRentalData[4] = $_POST['rentalBegin'];
  $carRentalData[5] = $_POST['rentalEnd'];
    return $carRentalData;
}

function getCarData(){
  $carData = array();
  $carData[1] = $_POST['vin'];
  $carData[2] = $_POST['licensePlate'];
  $carData[3] = $_POST['mileage'];
  $carData[4] = $_POST['year'];
  $carData[5] = $_POST['make'];
  $carData[6] = $_POST['model'];
  $carData[7] = $_POST['horsepower'];
  $carData[8] = $_POST['costPerDay'];
  $carData[9] = $_POST['suv'];
  $carData[10] = $_POST['drivetrain'];
  $carData[11] = $_POST['cargoCap'];
  $carData[12] = $_POST['sedan'];
  $carData[13] = $_POST['fuelType'];
  $carData[14] = $_POST['mpg'];
  $carData[15] = $_POST['sunroof'];
  $carData[16] = $_POST['truck'];
  $carData[17] = $_POST['towCap'];
  $carData[18] = $_POST['payloadCap'];
  $carData[19] = $_POST['bedLen'];
  $carData[20] = $_POST['numSeats'];
    return $carData;
}

function getCustomerData(){
  $customerData = array();
  $customerData[1] = $_POST['custID'];
  $customerData[2] = $_POST['fname'];
  $customerData[3] = $_POST['lname'];
  $customerData[4] = $_POST['addr1'];
  $customerData[5] = $_POST['addr2'];
  $customerData[6] = $_POST['city'];
  $customerData[7] = $_POST['state'];
  $customerData[8] = $_POST['zip'];
  $customerData[9] = $_POST['dob'];
    return $customerData;
}

  if(isset($_POST['carRentalButton'])){
    $info = getCarRentalData();
    $insert = "insert into CAR_RENTAL ([vin]
      ,[id_number]
      ,[transaction_number]
      ,[rentalBeginDate]
      ,[rentalReturnDate]) values ('$info[1]',
      '$info[2]',
      '$info[3]',
      '$info[4]',
      '$info[5]');";

      try{
        $connection = OpenConnection();
  
        $insertReview = sqlsrv_query($connection, $insert);
        if($insertReview == FALSE)
          die();
  
          echo "Car rental for car with VIN {$info[1]} and Customer with ID # {$info[2]} has been added to the database per transanction number {$info[3]}";
          sqlsrv_free_stmt($insertReview);
          sqlsrv_close($connection);
      }
      catch(Exception $e)
      {
        echo("Oh no!");
      }    
  }

  elseif (isset($_POST['carButton'])) {
    $info = getCarData();
    $insert = "insert into CAR ([vin]
      ,[licensePlate]
      ,[mileage]
      ,[model]
      ,[make]
      ,[year]
      ,[horsepower]
      ,[costPerDay]
      ,[isSuv]
      ,[drivetrain]
      ,[cargoCapacity]
      ,[isSedan]
      ,[fuelType]
      ,[mpg]
      ,[hasSunroof]
      ,[isTruck]
      ,[towCapacity]
      ,[payloadCapacity]
      ,[bedLength]
      ,[numSeats]) values ('$info[1]',
      '$info[2]',
      '$info[3]',
      '$info[6]',
      '$info[5]',
      '$info[4]',
      '$info[7]',
      '$info[8]',
      '$info[9]',
      '$info[10]',
      '$info[11]',
      '$info[12]',
      '$info[13]',
      '$info[14]',
      '$info[15]',
      '$info[16]',
      '$info[17]',
      '$info[18]',
      '$info[19]',
      '$info[20]');";

    try{
      $connection = OpenConnection();

      $insertReview = sqlsrv_query($connection, $insert);
      if($insertReview == FALSE)
        die();

        echo "{$info[5]} {$info[6]} with VIN {$info[1]} added to database";
        sqlsrv_free_stmt($insertReview);
        sqlsrv_close($connection);
    }
    catch(Exception $e)
    {
      echo("Oh no!");
    }    
  }

  elseif (isset($_POST['customerButton'])){
    $info = getCustomerData();
    $insert = "insert into CUSTOMER ([id_number]
      ,[address1]
      ,[address2]
      ,[city]
      ,[state]
      ,[zip]
      ,[dob]
      ,[fname]
      ,[lname]) values ('$info[1]',
      '$info[4]',
      '$info[5]',
      '$info[6]',
      '$info[7]',
      '$info[8]',
      '$info[9]',
      '$info[2]',
      '$info[3]');";

      try{
        $connection = OpenConnection();
  
        $insertReview = sqlsrv_query($connection, $insert);
        if($insertReview == FALSE)
          die();
  
          echo "{$info[2]} {$info[3]} with ID # {$info[1]} has been added to the database";
          sqlsrv_free_stmt($insertReview);
          sqlsrv_close($connection);
      }
      catch(Exception $e)
      {
        echo("Oh no!");
      }    
  }
?>


<!DOCTYPE html>
<html lang="en">
<head>
  <title>DB Wheels</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
  
<style type="text/css">
  #banner{
    background-color: #000;
    background-image: url(checker.jpg);
    background-position: center center;
    background-repeat: repeat;
    height: 50px;
    padding-bottom: 5px;
    padding-left: 10px;
  }
  #banner-text{
    font-weight:bold;
    color: #7d020f;
  }
  #table-header{
    font-weight: bold;
  }
</style>

<div class="jumbotron-fluid">
  <div class="container-fluid" id="banner">
    <h2 class="display-4" id="banner-text"><center>DB Wheels</center></h2>

  </div>
</div>

<div class="container">
  <form method="POST">
    <div class="row">
      <div class="col-sm-4">
        <h3 id="table-header"><center>Car Rental</center></h3>
        <div class="form-group">        
          <label for="usr">Car VIN:</label>
          <input type="text" class="form-control" id="vin" name="vin">
        </div>
        <div class="form-group">
          <label for="usr">Customer ID Number:</label>
          <input type="text" class="form-control" id="custID" name="custID">
        </div>
        <div class="form-group">
          <label for="usr">Transaction Number:</label>
          <input type="text" class="form-control" id="transNum" name="transNum">
        </div>
        <div class="form-group">
          <label for="usr">Rental Begin Date:</label>
          <input type="date" class="form-control" id="rentalBegin" name="rentalBegin">
        </div>
        <div class="form-group">
          <label for="usr">Rental End Date:</label>
          <input type="date" class="form-control" id="rentalEnd" name="rentalEnd">
        </div>
        <br />
        <button type="submit" class="btn btn-primary" name="carRentalButton">Insert Car Rental</button>
      </div>
      <div class="col-sm-4">
        <h3 id="table-header"><center>Car</center></h3>
        <div class="form-group">
          <label for="usr">Car VIN:</label>
          <input type="text" class="form-control" id="vin" name="vin">
        </div>
        <div class="form-group">
          <label for="usr">License Plate:</label>
          <input type="text" class="form-control" id="licensePlate" name="licensePlate">
        </div>
        <div class="form-group">
          <label for="usr">Mileage:</label>
          <input type="number" class="form-control" id="mileage" name="mileage">
        </div>
        <div class="form-group">
          <label for="usr">Year:</label>
          <input type="number" class="form-control" id="year" name="year">
        </div>
        <div class="form-group">
          <label for="usr">Make:</label>
          <input type="text" class="form-control" id="make" name="make">
        </div>
        <div class="form-group">
          <label for="usr">Model:</label>
          <input type="text" class="form-control" id="model" name="model">
        </div>
        <div class="form-group">
          <label for="usr">Horsepower:</label>
          <input type="number" class="form-control" id="horsepower" name="horsepower">
        </div>
        <div class="form-group">
          <label for="usr">Cost Per Day:</label>
          <input type="number" class="form-control" id="costPerDay" name="costPerDay">
        </div>
        <h3>Is SUV?</h3>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="suv" value=1>Yes
          </label>
        </div>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="suv" value=0>No
          </label>
        </div>
        <br />
        <h3>Drivetrain:</h3>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="drivetrain" value="FWD">FWD
          </label>
        </div>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="drivetrain" value="RWD">RWD
          </label>
        </div>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="drivetrain" value="4WD">4WD
          </label>
        </div>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="drivetrain" value="AWD">AWD
          </label>
        </div>
        <br />
        <div class="form-group">
          <label for="usr">Cargo Capacity:</label>
          <input type="number" step="0.1" class="form-control" id="cargoCap" name="cargoCap">
        </div>
        <h3>Is Sedan?</h3>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="sedan" value=1>Yes
          </label>
        </div>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="sedan" value=0>No
          </label>
        </div>
        <br />
        <div class="form-group">
          <label for="usr">Fuel Type:</label>
          <input type="text" class="form-control" id="fuelType" name="fuelType">
        </div>
        <div class="form-group">
          <label for="usr">Miles Per Gallon:</label>
          <input type="number" class="form-control" id="mpg" name="mpg">
        </div>
        <h3>Has Sunroof?</h3>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="sunroof" value=1>Yes
          </label>
        </div>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="sunroof" value=0>No
          </label>
        </div>
        <br />
        <h3>Is Truck?</h3>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="truck" value=1>Yes
          </label>
        </div>
        <div class="form-check">
          <label class="form-check-label">
            <input type="radio" class="form-check-input" name="truck" value=0>No
          </label>
        </div>
        <br />
        <div class="form-group">
          <label for="usr">Tow Capacity:</label>
          <input type="number" class="form-control" id="towCap" name="towCap">
        </div>
        <div class="form-group">
          <label for="usr">Payload Capacity:</label>
          <input type="number" class="form-control" id="payloadCap" name = "payloadCap">
        </div>
        <div class="form-group">
          <label for="usr">Bed Length:</label>
          <input type="number" class="form-control" id="bedLen" name = "bedLen">
        </div>
        <div class="form-group">
          <label for="usr">Number of Seats:</label>
          <input type="number" class="form-control" id="numSeats" name="numSeats">
        </div>
        <br />
        <button type="submit" class="btn btn-primary" name="carButton">Insert Car</button>
      </div>
      <div class="col-sm-4">
        <h3 id="table-header"><center>Customer</center></h3>
        <div class="form-group">
          <label for="usr">ID Number:</label>
          <input type="text" class="form-control" id="custID" name="custID">
        </div>
        <div class="form-group">
          <label for="usr">First Name:</label>
          <input type="text" class="form-control" id="fname" name="fname">
        </div>
        <div class="form-group">
          <label for="usr">Last Name:</label>
          <input type="text" class="form-control" id="lname" name="lname">
        </div>
        <div class="form-group">
          <label for="usr">Address Line 1:</label>
          <input type="text" class="form-control" id="addr1" name="addr1">
        </div>
        <div class="form-group">
          <label for="usr">Address Line 2:</label>
          <input type="text" class="form-control" id="addr2" name="addr2">
        </div>
        <div class="form-group">
          <label for="usr">City:</label>
          <input type="text" class="form-control" id="city" name="city">
        </div>
        <div class="form-group">
          <label for="usr">State:</label>
          <input type="text" class="form-control" id="state" name="state">
        </div>
        <div class="form-group">
          <label for="usr">Zip:</label>
          <input type="text" class="form-control" id="zip" name="zip">
        </div>
        <div class="form-group">
          <label for="usr">Date of Birth:</label>
          <input type="date" class="form-control" id="dob" name="dob">
        </div>      
        <br />
        <button type="submit" class="btn btn-primary" name="customerButton">Insert Customer</button>
      </div>
    </div>
  </form>
</div>

</body>
</html>
