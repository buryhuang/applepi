//
//  ViewController.swift
//  MyApplePi
//
//  Created by Bury Huang on 6/17/17.
//  Copyright © 2017 Null. All rights reserved.
//

import UIKit
import Foundation
import Photos

class ViewController: UIViewController, UIPickerViewDataSource, UIPickerViewDelegate {

    @IBOutlet weak var theLabel: UILabel!
    @IBOutlet weak var theIP: UIPickerView!
    
    var pickerData: [String] = [String]()

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        pickerData = ["192.168.42.1", "192.168.3.247", "192.168.3.248"]
        // Connect data:
        self.theIP.delegate = self
        self.theIP.dataSource = self
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @available(iOS 2.0, *)
    public func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        return pickerData[row]
    }

    // returns the number of 'columns' to display.
    @available(iOS 2.0, *)
    public func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    // returns the # of rows in each component..
    @available(iOS 2.0, *)
    public func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {

        return pickerData.count
    }


    @IBAction func theClick(_ sender: UIButton) {
        //let todoEndpoint: String = "https://jsonplaceholder.typicode.com/todos/1"
        //let todoEndpoint: String = "http://ec2-54-153-105-85.us-west-1.compute.amazonaws.com/todo/api/v1.0/tasks/3923100000"
        var todoEndpoint: String;
        // let targetHost : String = "192.168.42.1"
        let targetHost : String = self.pickerData[theIP.selectedRow(inComponent:0)]
        let baseUrlTask : String = "http://" + targetHost + "/applepi/api/v1.0/tasks/"
        
        theLabel.text = "Sending request to ... " + targetHost
        if (sender.titleLabel?.text == "Power Off") {
            todoEndpoint = baseUrlTask + "poweroff"
        } else if (sender.titleLabel?.text == "List") {
            todoEndpoint = baseUrlTask + "list"
        } else if (sender.titleLabel?.text == "Backup") {
            let fetchOptions: PHFetchOptions = PHFetchOptions()
            fetchOptions.sortDescriptors = [NSSortDescriptor(key: "creationDate", ascending: false)]
            //let fetchResult = PHAsset.fetchAssets(with: .video, options: fetchOptions)
            let fetchResult = PHAsset.fetchAssets(with: .image, options: fetchOptions)
            fetchResult.enumerateObjects(using: { (object, index, stop) -> Void in
                let options = PHImageRequestOptions()
                options.isSynchronous = true
                options.deliveryMode = .highQualityFormat
                PHImageManager.default().requestImageData(for: object, options: options, resultHandler:
                    {
                        (imageData: Data?, dataUTI: String?, orientation: UIImageOrientation, info: [AnyHashable : Any]?) in
                    
                        // If the image data is not nil, set it into the image view
                        if (imageData != nil) {
                            // Get image from the imageData
                            let image = UIImage.init(data: imageData!)
                            print(imageData as Any)
                        } else {
                        
                            // TODO: Error retrieving the image. Show alert
                            print("There was an error retrieving the image!\n")
                        }
                    }
                )
            }
            )
            return
        } else {
            theLabel.text = "Not a valid action"
            return
        }
        
        guard let url = URL(string: todoEndpoint) else {
            print("Error: cannot create URL")
            return
        }

        let urlRequest = URLRequest(url: url)
        let session = URLSession.shared
        let task = session.dataTask(with: urlRequest) {
            (data, response, error) in
            // check for any errors
            guard error == nil else {
                print("error calling GET on /todos/1")
                print(error!)
                return
            }
            // make sure we got data
            guard let responseData = data else {
                print("Error: did not receive data")
                return
            }
            // parse the result as JSON, since that's what the API provides
            do {
                guard let todo = try JSONSerialization.jsonObject(with: responseData, options: [])
                    as? [String: Any] else {
                        print("error trying to convert data to JSON")
                        return
                }
                // now we have the todo
                // let's just print it to prove we can access it
                print("The todo is: " + todo.description)
                DispatchQueue.main.async {
                    self.theLabel.text = todo.description
                }
                
                // the todo object is a dictionary
                // so we just access the title using the "title" key
                // so check for a title and print it if we have one
                guard let todoTitle = todo["title"] as? String else {
                    print("Could not get todo title from JSON")
                    return
                }
                //print("The title is: " + todoTitle)
            } catch  {
                print("error trying to convert data to JSON")
                return
            }
        }
        task.resume()
    }
}

