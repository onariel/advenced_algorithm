def Intersection(set1,set2):
    if len(set1) > len(set2):
        set3 = set2
        set2 = set1
        set1 = set3
    
    intersection_set = set()
    for friend_id in set1:
        if friend_id in set2:
            intersection_set.add(friend_id)
    return intersection_set


def Difference(set1,set2):
    difference_set = set()
    for friend_id in set1:
        if friend_id not in set2:
            difference_set.add(friend_id)
    return difference_set

def Union(set1,set2):
    union_set = set(set1)
    for friend_id in set2:
        if friend_id not in union_set:
            union_set.add(friend_id)
    return union_set


def friendCoef(set1,set2):
    intersection = Intersection(set1,set2)
    union = Union(set1,set2)
    len_intersection = len(intersection)
    len_union = len(union)
    if len_union == 0:
        return 0.0 
    else:
        return len_intersection / len_union



def findFriendSuggestions(UserId,allUserFriendsMap):
    targetUserFriends = allUserFriendsMap[UserId]
    suggestions = set()
    for friend_id in targetUserFriends:
        if friend_id not in allUserFriendsMap:
            continue
        friendsOfFriend = allUserFriendsMap[friend_id]
        for additionFriend in friendsOfFriend:
            if additionFriend not in targetUserFriends and additionFriend != UserId:
                suggestions.add(additionFriend)
    return suggestions



# Tests
if __name__ == "__main__":
    
    user_103_friends = {101, 102, 103, 104, 105, 106, 107, 108}  
    user_104_friends = {103, 104, 106, 107, 108}                
    user_a_friends = {101, 102, 103, 104, 105}                  
    user_b_friends = {103, 104, 106, 107, 108}                  
    all_user_friends = {
        "User A": user_a_friends,
        "User B": user_b_friends,
        103: user_103_friends,
        104: user_104_friends
    }

    # Test for function Intersection
    mutual_friends = Intersection(user_a_friends, user_b_friends)
    print(f"Mutual friends : {sorted(mutual_friends)}") 
    assert mutual_friends == {103, 104}, "Intersection error"


     # Test for funciton Difference
    unique_to_a = Difference(user_a_friends, user_b_friends)
    unique_to_b = Difference(user_b_friends, user_a_friends)
    print(f"Unique to A : {sorted(unique_to_a)}")
    print(f"Unique to B : {sorted(unique_to_b)}")
    assert unique_to_a == {101, 102, 105}, "Unique to A error"
    assert unique_to_b == {106, 107, 108}, "Unique to B error"

     #Test for function Union
    union_set = Union(user_a_friends, user_b_friends)
    print(f"Union: {sorted(union_set)}")
    assert len(union_set) == 8, "union error"

    #Test for function friendCoef
    jaccard_similarity = friendCoef(user_a_friends, user_b_friends)
    print(f"Jaccard similarity : {jaccard_similarity} ")
    assert abs(jaccard_similarity - 0.25) < 1e-6, "friendCoef error"

    #Test for function findFriendSuggestions
    a_suggestions = findFriendSuggestions("User A", all_user_friends)
    print(f"User A friend suggestions : {sorted(a_suggestions)}")
    assert a_suggestions == {106, 107, 108}, "Suggestions error"




    print("Start Boundary Testing")
    # empty set test
    empty_set = set()
    assert Intersection(empty_set, empty_set) == set(), "Empty Intersection error"
    assert Union(empty_set, empty_set) == set(), "Empty Union error"
    assert Difference(empty_set, empty_set) == set(), "Empty Difference error"
    assert friendCoef(empty_set, empty_set) == 0.0, "Empty friendCoef error"
    print("✔ Empty set test passed")


    # no union test
    set_x = {1,2}
    set_y = {3,4}
    assert Intersection(set_x, set_y) == set(), "No Intersection error"
    assert friendCoef(set_x, set_y) == 0.0, "No friendCoef error"
    print("✔ No common friends test passed")

    # unknownUser test
    try:
        findFriendSuggestions("UnknownUser", all_user_friends)
        assert False, "Should raise KeyError"
    except KeyError:
        print("✔ Unknown user test passed")


    # user no friend test
    all_user_friends[999] = set()
    suggestions = findFriendSuggestions(999, all_user_friends)
    assert suggestions == set(), "User with no friends error"
    print("✔ User with no friends test passed")