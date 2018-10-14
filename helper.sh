#!/usr/bin/env bash
# see README.md for use


# argument
if [ $1 ]; then
  case $1 in

    # test
    test)
      printf "Running tests...\n"
      if  [ $2 ]; then
        printf "looking for tests with '*test_$2*'...\n\n"
        python3 -m unittest discover -s "test_finData" -v -p "*test_$2*"
      else
        printf "running all tests ...\n\n"
        python3 -m unittest discover -s "test_finData" -v
      fi
      ;;

  esac

# no argument
else
  printf "no argument given\n\n"
fi
