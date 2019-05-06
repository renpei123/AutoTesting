   DEV)
sourceSERVER=dstbld-pda02.bld.dst.ibm.com
sourceDBName=BACC_DEV_SIW_SIWODS
export NZ_USER=$3
export NZ_PASSWORD=$4
   ;;
   TST)
sourceSERVER=netezza-1.boulder.ibm.com
sourceDBName=BACC_TST_SIW_SIWODS
export NZ_USER=$3
export NZ_PASSWORD=$4
   ;;
   PRD)
sourceSERVER=pda2-wall.boulder.ibm.com
sourceDBName=BACC_PRD_SIW_SIWODS
export NZ_USER=$3
export NZ_PASSWORD=$4
export USER=$NZ_USER
export PASSWD=$NZ_PASSWORD

   ;;
   *)
echo "No environment type has been specified. Please execute the script with the following parameters: "
echo "./AutoTestView.sh <Env> <view_list_file> <user> <pass>"
echo "example: "
echo "./AutoTestView.sh TST views.list siwadm *****"
exit 0;
   ;;
esac

if [[ ! $NZ_USER || ! $NZ_PASSWORD ]]
then
  echo "Usage: Make sure that the following variables are set: ./AutoTestView.sh <Env> <view_list_file> <user> <pass>"
  exit
fi

#####################################
# Extract permissions from Source DB
#####################################

export NZ_HOST=$sourceSERVER
export NZ_DATABASE=$sourceDBName


while read view
do

        echo "Testing view: $view"

        nz_get_view_rowcount $sourceDBName $view

done < $2
