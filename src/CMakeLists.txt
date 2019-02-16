#find_library(MGL mgl PATHS /usr/local/lib)

ADD_EXECUTABLE( iTrack main.cpp findEyeCenter.cpp findEyeCenter.h findEyeCorner.cpp findEyeCorner.h constants.h helpers.cpp helpers.h history.h)
TARGET_LINK_LIBRARIES( iTrack ${OpenCV_LIBS} )
#target_link_libraries( iTrack ${MGL})