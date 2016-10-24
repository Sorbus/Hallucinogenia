def check_range(value):
  ivalue = int(value)
  if ivalue < 0 or ivalue > 3:
   raise argparse.ArgumentTypeError("%s is not in range" % value)
  return ivalue    