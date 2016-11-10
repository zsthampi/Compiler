#include <stdio.h>
#define read(x) scanf("%d",&x)
#define write(x) printf("%d\n",x)
#define print(x) printf(x)

int getinput(void)
{
    int a;
    a = 0;
    while (0 >= a)
    {
	read(a);
	if (0 > a)
	{
	    print("I need a positive number: ");
	}
    }

    return a;
}

int main() 
{
    int coneradius, coneheight;
    int circleradius;
    int trianglebase, triangleheight;
    int sphereradius;

    int cone, circle, triangle, sphere;
    int pi;
    pi = 3141;

    print("Give me a radius for the base of a cone: ");
    coneradius = getinput();
    print("Give me a height for a cone: ");
    coneheight = getinput();
    print("Give me a radius for a circle: ");
    circleradius = getinput();
    print("Give me a length for the base of a triangle: ");
    trianglebase = getinput();
    print("Give me a height for a triangle: ");
    triangleheight = getinput();
    print("Give me a radius for a sphere: ");
    sphereradius = getinput();

    cone = (pi*coneradius*coneradius*coneheight + 500) / 3000;
    circle = (pi*circleradius*circleradius + 500) / 1000;
    triangle = (trianglebase*triangleheight) / 2;
    sphere = (4*pi*sphereradius*sphereradius*sphereradius+500) / 3000;

    print("The volume of the cone is: ");
    write(cone);
    print("The area of the circle is: ");
    write(circle);
    print("The area of the triangle is: ");
    write(triangle);
    print("The volume of the sphere is: ");
    write(sphere);
}
