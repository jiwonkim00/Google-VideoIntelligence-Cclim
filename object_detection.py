#!/usr/bin/env python
# coding: utf-8

# In[3]:


import io

def detect_objects(local_file_path="path/to/your/video-file.mp4"):
    path = local_file_path
    video_name = path.split('/')[-1]
    found_objects = {}

    """Object tracking in a local video."""
    from google.cloud import videointelligence

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.OBJECT_TRACKING]

    with io.open(path, "rb") as file:
        input_content = file.read()

    operation = video_client.annotate_video(
        request={"features": features, "input_content": input_content}
    )
    print("\nProcessing ", video_name, " for object annotations.")

    result = operation.result(timeout=300)
    print("\nFinished processing.\n")

    # The first result is retrieved because a single video was processed.
    object_annotations = result.annotation_results[0].object_annotations

    ## TODO : edit inside the for loop to only get number of certain objects
    for object_annotation in object_annotations:
        #object_annotation = object_annotations[annotation]   #0
        
        """ Count number of different objects detected """
        if str(object_annotation.entity.description) in found_objects :
            found_objects[str(object_annotation.entity.description)] += 1
        else :
            found_objects[str(object_annotation.entity.description)] = 1
        
        """ Print specific object information """
        print("Entity description: {}".format(object_annotation.entity.description))
        
        # if object_annotation.entity.entity_id:
        #     print("Entity id: {}".format(object_annotation.entity.entity_id))

        print(
            "Segment: {}s to {}s".format(
                object_annotation.segment.start_time_offset.seconds
                + object_annotation.segment.start_time_offset.microseconds / 1e6,
                object_annotation.segment.end_time_offset.seconds
                + object_annotation.segment.end_time_offset.microseconds / 1e6,
            )
        )

        print("Confidence: {}\n".format(object_annotation.confidence))

    print("SUMMARY; Counts in ", video_name, " : \n")
    for key_name in found_objects.keys() :
        print(key_name, " : ", found_objects[key_name])

    print('\n')


    """ Here we print only the bounding box of the first frame in this segment """

    # frame = object_annotation.frames[0]
    # box = frame.normalized_bounding_box
    # print(
    #     "Time offset of the first frame: {}s".format(
    #         frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
    #     )
    # )
    # print("Bounding box position:")
    # print("\tleft  : {}".format(box.left))
    # print("\ttop   : {}".format(box.top))
    # print("\tright : {}".format(box.right))
    # print("\tbottom: {}".format(box.bottom))
    # print("\n")
detect_objects("/Users/mac/Desktop/test_1.mp4")
detect_objects("/Users/mac/Desktop/test_2.mp4")
detect_objects("/Users/mac/Desktop/test_3.mp4")

