 /**
*/
#include <ctime>
#include <fstream>
#include <iostream>
#include <raspicam/raspicam.h>
using namespace std;
 
int main ( int argc,char **argv ) {
    raspicam::RaspiCam Camera; //Cmaera object
    //Open camera 
    cout<<"Opening Camera..."<<endl;
    if ( !Camera.open()) {cerr<<"Error opening camera"<<endl;return -1;}
    //wait a while until camera stabilizes
    cout<<"Sleeping for 3 secs"<<endl;
    sleep(3);
    //capture
    Camera.grab();
    //allocate memory
    unsigned char *data=new unsigned char[  Camera.getImageTypeSize ( raspicam::RASPICAM_FORMAT_RGB )];
    //extract the image in rgb format
    Camera.retrieve ( data,raspicam::RASPICAM_FORMAT_RGB );//get camera image
    //save
    std::ofstream outFile ( "raspicam_image.ppm",std::ios::binary );
    outFile<<"P6\n"<<Camera.getWidth() <<" "<<Camera.getHeight() <<" 255\n";
    outFile.write ( ( char* ) data, Camera.getImageTypeSize ( raspicam::RASPICAM_FORMAT_RGB ) );
    cout<<"Image saved at raspicam_image.ppm"<<endl;
    //free resrources    
    delete data;
    return 0;
}
 
/***********************************************************************
For cmake users,  create a file named CMakeLists.txt and add:
#####################################
cmake_minimum_required (VERSION 2.8) 
project (raspicam_test)
find_package(raspicam REQUIRED)
add_executable (simpletest_raspicam simpletest_raspicam.cpp)  
target_link_libraries (simpletest_raspicam ${raspicam_LIBS})
#####################################
 
Finally, create build dir,compile and execute
mkdir build
cd build
cmake ..
make
./simpletest_raspicam
 
If you do not like cmake, simply 
g++ simpletest_raspicam.cpp -o simpletest_raspicam -I/usr/local/include -lraspicam -lmmal -lmmal_core -lmmal_util

***********************************************************************/
