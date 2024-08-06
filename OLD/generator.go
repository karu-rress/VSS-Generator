// [[Deprecated]]
//
// generator.go
//
// This file is used to generate random vehicle data and store it in JSON files.
// The data generated includes the car ID, speed, location, fuel level, and engine temperature.
// The number of cars and number of JSON files per car can be specified as command line arguments.
// The generated JSON files are stored in directories named Car1, Car2, ..., CarN.
// Each JSON file is named as <car_id>-<file_number>.json.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"math/rand"
	"os"
	"path/filepath"
)

type Vehicle struct {
	CarID     string    `json:"car_id"`
	Speed     Speed     `json:"Speed"`
	Location  Location  `json:"Location"`
	FuelLevel FuelLevel `json:"FuelLevel"`
	Engine    Engine    `json:"Engine"`
}

type Speed struct {
	Value int    `json:"value"`
	Unit  string `json:"unit"`
}

type Location struct {
	Latitude  float64 `json:"Latitude"`
	Longitude float64 `json:"Longitude"`
}

type FuelLevel struct {
	Value float64 `json:"value"`
	Unit  string  `json:"unit"`
}

type Engine struct {
	Temperature Temperature `json:"Temperature"`
}

type Temperature struct {
	Value float64 `json:"value"`
	Unit  string  `json:"unit"`
}

func randomVehicle(id int) Vehicle {
	const (
		MAX_SPEED = 120
		WEST      = 33
		EAST      = 43
		NORTH     = 132
		SOUTH     = 124
		MAX_TEMP  = 120
	)

	carID := fmt.Sprintf("car_%d", id)
	speed := Speed{
		Value: rand.Intn(MAX_SPEED + 1), // 0 to MAX_SPEED km/h
		Unit:  "km/h",
	}
	location := Location{
		// Latitude: WEST to EAST
		Latitude:  rand.Float64()*float64(EAST-WEST) + float64(WEST),
		Longitude: rand.Float64()*float64(NORTH-SOUTH) + float64(SOUTH),
	}
	fuelLevel := FuelLevel{
		Value: rand.Float64() * 100, // 0 to 100%
		Unit:  "%",
	}
	engineTemperature := Engine{
		Temperature: Temperature{
			Value: float64(rand.Intn(MAX_TEMP)), // 0 to MAX_TEMP °C
			Unit:  "°C",
		},
	}

	return Vehicle{
		CarID:     carID,
		Speed:     speed,
		Location:  location,
		FuelLevel: fuelLevel,
		Engine:    engineTemperature,
	}
}

func main() {
	numCars := flag.Int("n_cars", 1, "Number of cars to generate")
	numFiles := flag.Int("n_files", 1, "Number of JSON files per car")
	changeRate := flag.Float64("rate", 0.2, "Rate of change of vehicle data")
	threshold := flag.Float64("threshold", 0.2, "Threshold for change of vehicle data")
	flag.Parse()

	// NOT USED in this version
	_, _ = changeRate, threshold

	if *numCars <= 0 || *numFiles <= 0 {
		fmt.Println("Please provide valid integers for both numCars and numFiles.")
		return
	}

	for i := 1; i <= *numCars; i++ {
		// Create directory for each car
		carDir := fmt.Sprintf("Car%d", i)
		err := os.MkdirAll(carDir, os.ModePerm)
		if err != nil {
			fmt.Println("Error creating directory:", err)
			return
		}

		for j := 1; j <= *numFiles; j++ {
			vehicle := randomVehicle(i)
			vehicleJSON, err := json.MarshalIndent(vehicle, "", "  ")
			if err != nil {
				fmt.Println("Error marshalling to JSON:", err)
				return
			}

			// Create JSON file
			fileName := filepath.Join(carDir, fmt.Sprintf("%d-%d.json", i, j))
			err = os.WriteFile(fileName, vehicleJSON, 0644)
			if err != nil {
				fmt.Println("Error writing to file:", err)
				return
			}
		}
	}
}
