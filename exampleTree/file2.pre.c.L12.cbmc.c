int func(int x, int y)
{
  int a = 0;
  float c = 1.0;
  char example[100];
  int b = 2 + y;
  y *= b;
  for (; (x > 3) || (y == 1); x--, y++)
  {
    if (b < 5)
    {
      b++;
      assert(0);
    }

    a++;
  }

  return a;
}

